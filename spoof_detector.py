from decimal import Decimal
import threading
from ibapi import wrapper
from ibapi.client import EClient, TickerId
from IBJts.source.pythonclient.ibapi.common import TickAttribLast
from IBJts.source.pythonclient.ibapi.contract import Contract
from lineplot import LevelTwoLinePlot
from heatmap import LevelTwoHeatmap
import argparse


class MessageReciever(wrapper.EWrapper):
    pass


class MessageSender(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class App(MessageReciever, MessageSender):
    def __init__(self, plot):
        self.lock = threading.Lock()
        MessageReciever.__init__(self)
        MessageSender.__init__(self, wrapper=self)
        self.plot = plot
        self.contract = self._future_contract()

    @staticmethod
    def _future_contract() -> Contract:
        contract = Contract()
        contract.symbol = "MES"
        contract.secType = "FUT"
        contract.exchange = "CME"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "202303"
        return contract

    def updateMktDepth(
        self,
        reqId: TickerId,
        position: int,
        operation: int,
        side: int,
        price: float,
        size: Decimal,
    ):
        super().updateMktDepth(reqId, position, operation, side, price, size)
        if side == 0:
            self.plot.add_ask(position, size)
        elif side == 1:
            self.plot.add_bid(position, size)

    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        self.reqMktDepth(1, self.contract, 10, False, [])
        self.reqTickByTickData(2, self.contract, "AllLast", 0, False)

    def tickByTickAllLast(
        self,
        reqId: int,
        tickType: int,
        time: int,
        price: float,
        size: Decimal,
        tickAtrribLast: TickAttribLast,
        exchange: str,
        specialConditions: str,
    ):
        super().tickByTickAllLast(
            reqId,
            tickType,
            time,
            price,
            size,
            tickAtrribLast,
            exchange,
            specialConditions,
        )
        self.plot.add_sale(size)

    def run(self):
        threading.Thread(target=lambda: super(App, self).run()).start()
        self.plot.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot")
    parser.add_argument("--length")
    args = parser.parse_args()
    plot = None
    if args.plot == "heatmap":
        plot = LevelTwoHeatmap(int(args.length))
    else:
        plot = LevelTwoLinePlot(int(args.length))
    app = App(plot=plot)
    app.connect("127.0.0.1", 7496, clientId=0)
    app.run()
