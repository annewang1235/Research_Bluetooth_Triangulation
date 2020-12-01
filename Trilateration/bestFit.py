import numpy as np
import matplotlib.pyplot as plt
import pylab

import subprocess
import json


def chooseDevice():
    output = subprocess.check_output("blueutil --format json --paired", shell=True)

    output_json = output.decode("utf-8").replace("'", '"')

    data = json.loads(output_json)
    device_arr = []
    index = 0

    device_name_arr = []
    for ele in data:
        print(index, ele["name"])
        device_name_arr.append(ele["name"])
        device_arr.append(ele["address"])
        index += 1

    chosen = input("Device #: ")
    return (device_arr[int(chosen)], device_name_arr[int(chosen)])


def getBestFitLine(device_name, bestFitLineList):
    # TODO: change file so that it's a bluetooth spreadsheet!
    # this method should account for ALL 6 BLUETOOTH MODULES (in a loop)
    with open("bluetooth_data_HC_01.csv") as f:
        next(f)
        data = [[line.split(",")[0], line.split(",")[1]] for line in f.readlines()]
        print(data)
        for (x, y) in data:
            plt.scatter(float(x), float(y))

        # TODO: update x- and y-labels and plot title for bluetooth!
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
        bestFitLineList.append((m, b))

        plt.show()

        print(bestFitLineList)
        return bestFitLineList


def getDistance(m, rssi, b):
    return (rssi - b) / m


if __name__ == "__main__":
    # convertCsvToTxt("HC_01")
    getBestFitLine("HC_01", [])
    # device_address, device_name = chooseDevice()