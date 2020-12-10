import numpy as np
import matplotlib.pyplot as plt
import pylab


def getBestFitLine(fileName, device_name, bestFitLineDict):
    with open(fileName) as f:
        next(f)
        data = [[line.split(",")[0], line.split(",")[1]] for line in f.readlines()]

        x_vals = np.array([float(x) for x, y in data])
        y_vals = np.array([float(y) for x, y in data])

        plotData(x_vals, y_vals, data)

        m, b = np.polyfit(x_vals, y_vals, 1)

        # device_name is the key
        bestFitLineDict[device_name] = (m, b)

        print(bestFitLineDict)
        return bestFitLineDict


def plotData(x_vals, y_vals, data):
    for (x, y) in data:
        plt.scatter(float(x), float(y))

    plt.xlabel("Distance (ft)")
    plt.ylabel("RSSI Values")
    plt.title("Distance Vs RSSI Values")

    plt.plot(
        np.unique(x_vals),
        np.poly1d(np.polyfit(x_vals, y_vals, 1))(np.unique(x_vals)),
    )

    plt.show()


def getDistance(m, rssi, b):
    return (rssi - b) / m
