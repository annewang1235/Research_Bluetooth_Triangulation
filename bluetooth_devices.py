import subprocess
import json
import time

import csv


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
    print("rawRSSI Stats For", distance, "Feet Away")
    print("RANGE:", rangeOfRSSI)
    print("MEAN:", mean)
    print("MEDIAN:", median)
    print("MODE:", mode)
    print()


if __name__ == "__main__":
    device_id, device_name = getDeviceID()

    # each device has its own specific spreadsheet, name of spreadsheet to include name of device
    with open("bluetooth_data_" + device_name + ".csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Distance (ft)", "Raw RSSI", "Range of RSSI", "Mean"])

        for i in range(1, 21):
            distance = input("Distance from beacon: ")
            samples = getRSSISamples(100, distance, device_id)

            # raw RSSI ranges
            raw_range = getRange(samples[1])

            # raw RSSI mean, median, mode
            raw_mean = getMean(samples[1])
            raw_median = getMedian(samples[1])
            raw_mode = getMode(samples[1])
            printData(distance, raw_range, raw_mean, raw_median, raw_mode)

            writer.writerow([distance, raw_median, raw_range, raw_mean])
