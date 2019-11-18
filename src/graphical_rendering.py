import numpy as np
from matplotlib import pyplot as plt


class GraphProcess:
    """render statistics as graph"""
    def __init__(self, title: str, url_name: str):
        self.title = title
        self.url_name = url_name

    def save_graph(self, data: dict) -> bytes:
        # with open('graph.json', 'w') as f:
        #     f.write(str(data))
        try:
            if isinstance(
                    data["payload"]["statistics_closed"]["90days"][0]["mod_rank"],
                    int
                    ):
                is_mod = True
        except Exception:
            is_mod = False
        y, z, d = [], [], []
        for i, stats in enumerate(data["payload"]["statistics_closed"]["90days"]):
            if is_mod:
                if i % 2 != 0:
                    y.append(stats["moving_avg"])
                    z.append(stats["avg_price"])
                    d.append(stats["volume"])
            else:
                y.append(stats["moving_avg"])
                z.append(stats["avg_price"])
                d.append(stats["volume"])

        x = np.arange(0, len(y))
        plt.figure(figsize=(8, 7))
        plt.subplot(2, 1, 1)
        plt.plot(x, y, "b-.")
        plt.plot(x, z, "r-")

        plt.title(self.title)
        plt.legend(["Moving average price", "Average selling price"])
        plt.xlabel("Time(last 90 days)")
        plt.ylabel("Prices(platinum)")

        plt.subplot(2, 1, 2)
        plt.bar(x, d, label="Bars")
        plt.legend(["Volume sold"])
        plt.xlabel("Time(last 90 days)")
        plt.ylabel("Volume")

        plt.savefig("graphs/"+self.url_name+".png")
        # plt.show()
