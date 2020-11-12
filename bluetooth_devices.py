import subprocess
import json
import time

import xlwt
from xlwt import Workbook

import csv


def getDeviceID():
    output = subprocess.check_output("blueutil --format json --paired", shell=True)

    output_json = output.decode("utf-8").replace("'", '"')

    data = json.loads(output_json)
    device_arr = []
    index = 0

    for ele in data:
        print(index, ele["name"])
        device_arr.append(ele["address"])
        index += 1

    chosen = input("Device #: ")
    return device_arr[int(chosen)]


def getRSSISamples(num_samples, distance, device_id):
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
        time.sleep(0.1)
        iter_num += 1
    return (sorted(samples), sorted(raw_samples))


def writeData(distance, median):
    with open("bluetooth_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        writer.writerow([distance, median])


def getMean(samples):
    sum = 0
    for sample in samples:
        sum += sample
    return sum / len(samples)


def getMedian(samples):
    if len(samples) % 2:
        return samples[len(samples) / 2]
    return (samples[(int(len(samples) / 2))] + samples[(int(len(samples) / 2)) - 1]) / 2


def getRange(samples):
    return (samples[0], samples[len(samples) - 1])


def getMode(samples):
    return max(set(samples), key=samples.count)


def printData(distance, rangeOfRSSI, mean, median, mode):
    print()
    print("RSSI Stats For", distance, "Feet Away")
    print("RANGE:", rangeOfRSSI)
    print("MEAN:", mean)
    print("MEDIAN:", median)
    print("MODE:", mode)
    print()


if __name__ == "__main__":
    device_id = getDeviceID()

    with open("bluetooth_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Distance (ft)", "RSSI", "Range of RSSI", "Mean"])

        for i in range(1, 21):
            distance = input("Distance from beacon: ")
            samples = getRSSISamples(100, distance, device_id)
            regular_range = getRange(samples[0])
            raw_range = getRange(samples[1])

            rangeOfRSSI = getRange(samples[0])
            mean = getMean(samples[0])
            median = getMedian(samples[0])
            mode = getMode(samples[0])
            printData(distance, rangeOfRSSI, mean, median, mode)

            writer.writerow([distance, median, rangeOfRSSI, mean])
