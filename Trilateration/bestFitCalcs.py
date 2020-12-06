import numpy as np
import matplotlib.pyplot as plt
import pylab


def getBestFitLine(fileName, device_name, bestFitLineDict):
    with open(fileName) as f:
        next(f)
        data = [[line.split(",")[0], line.split(",")[1]] for line in f.readlines()]

        for (x, y) in data:
            plt.scatter(float(x), float(y))

        plt.xlabel("Distance (ft)")
        plt.ylabel("RSSI Values")
        plt.title("Distance Vs RSSI Values")

        x_vals = np.array([float(x) for x, y in data])
        y_vals = np.array([float(y) for x, y in data])

        plt.plot(
            np.unique(x_vals),
            np.poly1d(np.polyfit(x_vals, y_vals, 1))(np.unique(x_vals)),
        )

        m, b = np.polyfit(x_vals, y_vals, 1)
        # # I wanna store m & b in a dictonary (as values in a list) and have the keys of this dictionary be...the
        # # number which identifies the bluetooth (like first one, second one, third one, etc)
        bestFitLineDict[device_name] = (m, b)

        plt.show()

        print(bestFitLineDict)
        return bestFitLineDict


def getDistance(m, rssi, b):
    return (rssi - b) / m
