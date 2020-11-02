import subprocess
import json
from collections import defaultdict
import time


def distanceStrength():

    output = subprocess.check_output(
        "blueutil --format json-pretty --paired", shell=True
    )

    # decodes the byte into a json
    output_json = output.decode("utf-8").replace("'", '"')

    data = json.loads(output_json)  # loads the json into a dictionary

    # there might be multiple connected devices -- we want to look for the bluetooth module
    for i in range(len(data)):
        if "HC-05" in data[i]["name"]:
            return (data[i], data[i]["address"])


def getRSSIdata(distance, distanceToStrength):

    ele, device_id = distanceStrength()

    if ele["connected"]:
        print(ele["name"], " ==> Signal strength: ", ele["RSSI"])

        distanceToStrength[distance].append(ele["RSSI"])
        distanceToStrength[distance].sort(reverse=True)

    else:
        print(ele["name"], " is not connected.")
        print("trying to connect")
        subprocess.check_output("blueutil --connect " + device_id, shell=True)
        print("check if connected?")


def getRange(length, distance, distanceToStrength):

    return (distanceToStrength[distance][0], distanceToStrength[distance][length - 1])


def getMedian(length, distance, distanceToStrength):
    midpoint = length // 2
    print("this is midpoint", midpoint)
    return distanceToStrength[distance][midpoint]


def getMean(length, distance, distanceToStrength):
    total = 0
    for val in distanceToStrength[distance]:
        total += val

    return total // length


if __name__ == "__main__":
    distanceToStrength = defaultdict(list)
    distance = input("Enter the distance: ")
    for i in range(100):

        getRSSIdata(distance, distanceToStrength)
        time.sleep(0.1)

    length = len(distanceToStrength[distance])
    print(distanceToStrength)
    rangeOfRSSIVals = getRange(length, distance, distanceToStrength)
    median = getMedian(length, distance, distanceToStrength)
    mean = getMean(length, distance, distanceToStrength)

    print("Range: ", rangeOfRSSIVals)
    print("Median:", median)
    print("Mean: ", mean)
