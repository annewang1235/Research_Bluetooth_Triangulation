import subprocess
import json
import time

import csv
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def getDeviceID():
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


def getRSSISamples(num_samples, device_id):
    iter_num = 0
    samples = []
    raw_samples = []
    subprocess.check_output("blueutil --connect " + device_id, shell=True)
    while iter_num < num_samples:
        output = subprocess.check_output(
            "blueutil --format json --info " + device_id, shell=True
        )

        output_json = output.decode("utf-8").replace("'", '"')

        data = json.loads(output_json)

        if data["connected"]:
            samples.append(data["RSSI"])
            raw_samples.append(data["rawRSSI"])
            print(data["name"], "Iteration Count:", iter_num + 1)
        else:
            print("disconnected. trying to reconnect.")
            subprocess.check_output("blueutil --connect " + device_id, shell=True)
            print("connected...continuing data collection")

        time.sleep(0.1)
        iter_num += 1
    return (sorted(samples), sorted(raw_samples))


def getMean(samples):
    sum = 0
    for sample in samples:
        sum += sample
    return sum / len(samples)


def getMedian(samples):
    if len(samples) % 2:
        return samples[len(samples) // 2]
    return (samples[(int(len(samples) / 2))] + samples[(int(len(samples) / 2)) - 1]) / 2


def getMode(samples):
    return max(set(samples), key=samples.count)


def rssi2dist(rssi, measuredPower, environFactor):
    print("test:",rssi,measuredPower,environFactor)
    predictDist = 10 ** ((measuredPower - rssi) / environFactor)

    return predictDist


def getEnvironFactor(x, y):
    result = curve_fit(func, x, y, method='trf')
    n, A = result[0]
    n = abs(n)

    return n, A


def printData(distance, mean, median, mode):
    print()
    print("rawRSSI Stats For", distance, "Meter(s) Away")
    print("MEAN:", mean)
    print("MEDIAN:", median)
    print("MODE:", mode)
    print()


def func(x, a, b):
    y = a * np.lib.scimath.log(x) + b
    return y



def plotFitData(x0, y0, data):
    for (x, y) in data:
        plt.scatter(float(x), float(y))

    plt.xlabel("Distance (m)")
    plt.ylabel("RSSI")
    plt.title("Distance Vs RSSI Values")

    result = curve_fit(func, x0, y0)
    n, A = result[0]

    x1 = np.arange(x0[0], x0[-1], 0.1)
    y1 = n * np.lib.scimath.log(x1) + A
    plt.plot(x1, y1, "blue")

    plt.show()


def print_grid(n, grid_values):
    print()
    print("\t\t\tTrilateration Grid\n")

    st = "   "
    for i in range(n):
        st = st + "     " + str(i)
    print(st)

    for r in range(n):
        st = "     "
        if r == 0:
            for col in range(n):
                st = st + "______"
            print(st)

        st = "     "
        for col in range(n):
            st = st + "|     "
        print(st + "|")

        st = "  " + str(r) + "  "
        for col in range(n):
            st = st + "|  " + str(grid_values[r][col]) + "  "
        print(st + "|")

        st = "     "
        for col in range(n):
            st = st + "|_____"
        print(st + '|')

    print()


if __name__ == "__main__":
    device_id, device_name = getDeviceID()
    times = int(input("Test Times: "))

    fileName = "data_" + device_name + ".csv"

    # each device has its own specific spreadsheet, name of spreadsheet to include name of device
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if os.stat(fileName).st_size == 0:
            writer.writerow(
                ["Distance (m)", "Raw RSSI Median", "Mean"]
            )

        for i in range(times):
            distance = input("Distance from beacon: ")
            samples = getRSSISamples(100, device_id)

            # raw RSSI mean, median, mode
            raw_mean = getMean(samples[1])
            raw_median = getMedian(samples[1])
            raw_mode = getMode(samples[1])
            printData(distance, raw_mean, raw_median, raw_mode)


            writer.writerow([distance, raw_median, raw_mean])

        csvfile.close()

    with open(fileName) as f:
        next(f)
        data = [[line.split(",")[0], line.split(",")[1]] for line in f.readlines()]

        x_vals = np.array([float(x) for x, y in data])
        y_vals = np.array([float(y) for x, y in data])

        plotFitData(x_vals, y_vals, data)
        n, A = getEnvironFactor(x_vals, y_vals)

        f.close()

    print("Environmental Factor:", n / 10)
    print("Measured Power:", A)
    input("Move the Beacon\nPress enter to continue...")
    print("Continuing...")
    newSamples = getRSSISamples(100, device_id)
    newSamplesRssi = getMedian(newSamples[1])
    print(newSamplesRssi)
    dist = rssi2dist(newSamplesRssi, A, n)

    print("Predicted Distance:", dist)

    n = 10 if int(dist) + 2 < 10 else int(dist) + 2
    grid_values = [[" " for x in range(n)] for y in range(n)]
    grid_values[0][0] = "L"
    grid_values[0][int(dist)] = "B"
    print_grid(n, grid_values)
