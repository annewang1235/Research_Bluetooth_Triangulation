import subprocess
import json
import time

import csv

import os


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


def getRSSISamples(num_samples, device_id): #accounts for calibrating data for multiple beacons at once
    iter_num = 0
    samples_dict = {}
    raw_samples_dict = {}
    for id in device_id:
      samples_dict[id] = []
      raw_samples_dict[id] = []
      subprocess.check_output("blueutil --connect " + id, shell=True)
    
    while iter_num < num_samples:
        output = subprocess.check_output(
            "blueutil --format json --paired", shell=True
        )

        output_json = output.decode("utf-8").replace("'", '"')

        data = json.loads(output_json)

        for device in data:
          if device["address"] in device_id:
            if device["connected"]:
                if (device["rawRSSI"] < 0):
                    samples_dict[device["address"]].append(device["RSSI"])
                    raw_samples_dict[device["address"]].append(device["rawRSSI"])
                    print(device["name"], "Iteration Count:", iter_num + 1)
                else: 
                    print(device["name"], "Weird RSSI reading:", device["rawRSSI"])
                    iter_num -= 1
            else:
                print("disconnected. trying to reconnect.")
                for id in device_id:
                  subprocess.check_output("blueutil --connect " + id, shell=True)
                
                print("connected...continuing data collection")
                # last sample is outlier if disconnected so we remove it
                # raw_samples[device["address"]].pop()
                # samples[device["address"]].pop()
                iter_num -= 1

        time.sleep(0.1)
        iter_num += 1
    
    # sorts each of our lists of data 
    for key in device_id:
      samples_dict[key].sort()
      raw_samples_dict[key].sort()

    return (samples_dict, raw_samples_dict)


def getMean(samples):
    sum = 0
    for sample in samples:
        sum += sample
    return sum / len(samples)


def getMedian(samples):
    if len(samples) % 2:
        return samples[len(samples) // 2]
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
    startVal = 3
    endVal = 20

    fileName = "rpi_" + device_name + ".csv"
    device_id = [device_id]
    print(device_id)

    # each device has its own specific spreadsheet, name of spreadsheet to include name of device
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if os.stat(fileName).st_size == 0:
            writer.writerow(
                ["Distance (ft)", "Raw RSSI Median", "Range of RSSI", "Mean"]
            )

        for i in range(startVal, endVal + 1):
            distance = input(f'{i} feet away from Beacon\npress enter to continue...')
            
            samples = getRSSISamples(100, device_id)
            print(samples[1][device_id[0]])

            # raw RSSI ranges
            raw_range = getRange(samples[1][device_id[0]])

            # raw RSSI mean, median, mode
            raw_mean = getMean(samples[1][device_id[0]])
            raw_median = getMedian(samples[1][device_id[0]])
            raw_mode = getMode(samples[1][device_id[0]])
            printData(i, raw_range, raw_mean, raw_median, raw_mode)

            writer.writerow([i, raw_median, raw_range, raw_mean])
