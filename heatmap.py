import threading
from matplotlib import animation
import numpy as np
import matplotlib.pyplot as plt


class LevelTwoHeatmap:
    def __init__(self, length) -> None:
        self.lock = threading.Lock()
        self.length = length
        self.current_orders = [0] * 20
        self.order_history = np.zeros((20, 1))
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(
            self.order_history,
            aspect="auto",
            extent=[0, self.length, 0, 20],
            vmin=0,
            vmax=100,
        )
        labels = [
            "bid10",
            "bid9",
            "bid8",
            "bid7",
            "bid6",
            "bid5",
            "bid4",
            "bid3",
            "bid2",
            "bid1",
            "ask1",
            "ask2",
            "ask3",
            "ask4",
            "ask5",
            "ask6",
            "ask7",
            "ask8",
            "ask9",
            "ask10",
        ]
        self.ax.set_yticks(np.arange(len(labels)), labels=labels)
        self.ax.set_ylabel("Level")
        self.ax.set_xlabel("Message")
        self.ax.set_title("Orders")
        self.fig.tight_layout()
        self.colorbar = self.fig.colorbar(self.im, ax=self.ax, label="Order size")
        self.anim = animation.FuncAnimation(
            self.fig,
            self._update_chart,
            interval=10,
            blit=True,
            frames=np.linspace(0, 2 * np.pi, 128),
        )

    def add_bid(self, position, size):
        if size == 0:
            return
        with self.lock:
            self.current_orders[10 + position] = int(size)
            self._update_current_orders()

    def add_ask(self, position, size):
        if size == 0:
            return
        with self.lock:
            self.current_orders[9 - position] = int(size)
            self._update_current_orders()

    def add_sale(self, size):
        pass

    def _update_current_orders(self):
        arr = np.resize(np.array(self.current_orders), (20, 1))
        self.order_history = np.append(self.order_history, arr, 1)
        if self.order_history.shape[1] > self.length:
            self.order_history = self.order_history[:, 1:]

    def _update_chart(self, i):
        with self.lock:
            self.im.set_data(self.order_history)
            self.colorbar.set_ticks(np.linspace(0, self.order_history.max(), num=5))
            self.colorbar.update_normal(self.im)
            return (self.im,)

    def show(self):
        plt.show()
