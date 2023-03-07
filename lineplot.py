import threading
from matplotlib import animation
import numpy as np
from matplotlib import pyplot


class LevelTwoLinePlot:
    def __init__(self, length):
        self.lock=threading.Lock()
        self.bids = [0] * 10
        self.asks = [0] * 10
        self.ask_history = []
        self.bid_history = []
        self.sale_history = [0]
        self.x_points = np.arange(length)
        self.figure, (self.lob_axis, self.volume_axis) = pyplot.subplots(
            nrows=2, ncols=1, sharex=True
        )
        self.lob_axis.set_title("Orders")
        self.volume_axis.set_title("Sales")
        (self.ask_line,) = self.lob_axis.plot([], [], "-", label="ask", color="red")
        (self.bid_line,) = self.lob_axis.plot([], [], "-", label="bid", color="green")
        (self.volume_line,) = self.volume_axis.plot(
            [], [], "-", label="volume", color="black"
        )
        self.lob_axis.legend(loc="upper left")
        self.anim = animation.FuncAnimation(
            self.figure,
            self._update_chart,
            interval=1,
            blit=True,
            frames=np.linspace(0, 2 * np.pi, 128),
        )
        self.lob_axis.set_ylim(0, 2000)
        self.lob_axis.set_xlim(0,length)
        self.volume_axis.set_ylim(0,40)
        self.volume_axis.set_xlim(0,length)


    def show(self):
        pyplot.show()

    def add_bid(self, position, size):
        with self.lock:
            self.bids[position] = size
            self.bid_history.append(sum(self.bids))
            if len(self.bid_history) > len(self.x_points):
                self.bid_history.pop(0)

    def add_ask(self, position, size):
        with self.lock:
            self.asks[position] = size
            self.ask_history.append(sum(self.asks))
            if len(self.ask_history) > len(self.x_points):
                self.ask_history.pop(0)

    def add_sale(self, size):
        self.sale_history.append(size)
        if len(self.sale_history) > len(self.x_points):
            self.sale_history.pop(0)

    def _update_chart(self, i):
        with self.lock:
            if (
                len(self.ask_history) != len(self.x_points)
                or len(self.bid_history) != len(self.x_points)
                or len(self.sale_history) != len(self.x_points)
            ):
                return (self.ask_line, self.bid_line, self.volume_line)
            self.ask_line.set_data(self.x_points, self.ask_history)
            self.bid_line.set_data(self.x_points, self.bid_history)
            self.volume_line.set_data(self.x_points, self.sale_history)
            #self.volume_axis.relim()
            #self.volume_axis.autoscale_view()
            return (self.ask_line, self.bid_line, self.volume_line)