#
# AUTHOR: Anne Wang (UC Irvine)
# DATE: UC Irvine Fall, November 2020
# PURPOSE: Research for Bluetooth Trilateration: Data Collection
# CONTACT: annew3@uci.edu
#


import subprocess
import json
from collections import defaultdict
import time


def distanceStrength(device_name):

    output = subprocess.check_output(
        "blueutil --format json-pretty --paired", shell=True
    )

    # decodes the byte into a json
    output_json = output.decode("utf-8").replace("'", '"')

    data = json.loads(output_json)  # loads the json into a dictionary

    # there might be multiple connected devices -- we want to look for the bluetooth module
    for i in range(len(data)):
        if ("HC_" + device_name) in data[i]["name"]:
            return (data[i], data[i]["address"])


def getRSSIdata(device_name, distance, distanceToStrength):

    ele, device_id = distanceStrength(device_name)

    if ele["connected"]:

        distanceToStrength[distance].append(ele["RSSI"])
        distanceToStrength[distance].sort(reverse=True)

    else:
        print(ele["name"], " is not connected.")
        print("trying to connect")
        subprocess.check_output("blueutil --connect " + device_id, shell=True)
        print("connected\n")


def getRange(length, distance, distanceToStrength):

    return (distanceToStrength[distance][0], distanceToStrength[distance][length - 1])


def getMedian(length, distance, distanceToStrength):
    midpoint = length // 2
    return distanceToStrength[distance][midpoint]


def getMean(length, distance, distanceToStrength):
    total = 0
    for val in distanceToStrength[distance]:
        total += val

    return total // length


def printData(distance, median, rangeOfRSSIVals, mean):
    print("Data for Distance:", distance, "feet away from bluetooth.")
    print("Median:", median, "\n")
    print("Range: ", rangeOfRSSIVals)
    print("Mean: ", mean)


if __name__ == "__main__":
    distanceToStrength = defaultdict(list)
    device_name = input("Enter in which device (integer): ")

    print("\nData for Device HC_" + device_name)
    for j in range(1, 21):
        distance = str(j)
        print("Start collecting data for distance:", distance, "feet away")

        for i in range(100):

            getRSSIdata(device_name, distance, distanceToStrength)
            time.sleep(0.1)

        length = len(distanceToStrength[distance])
        rangeOfRSSIVals = getRange(length, distance, distanceToStrength)
        median = getMedian(length, distance, distanceToStrength)
        mean = getMean(length, distance, distanceToStrength)

        printData(distance, median, rangeOfRSSIVals, mean)

        print("TIME TO MOVE.\n")
        time.sleep(3)
