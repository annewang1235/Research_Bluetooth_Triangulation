import Trilateration.inputs as inputs
import Trilateration.bestFitCalcs as bestFitCalcs
import Trilateration.output as output
import bluetooth_devices
import draw_circle
from collections import defaultdict
import matplotlib.pyplot as plt

import math

import csv

import os


def collectDataSamples(bestFitLineDict, device_name, device_id):
    for j in range(20):
      # gets the RSSI data from specified device
      samples, raw_samples = bluetooth_devices.getRSSISamples(50, device_id)

      # gets the RSSI mode and distance between receiver & i's device
      rssi_median = {key:bluetooth_devices.getMedian(raw_sample) for (key, raw_sample) in raw_samples.items()}
      print("rssi_mode is " + str(rssi_median))

      for index in range(len(device_name)):
        predicted_distance = bestFitCalcs.getDistance(
            bestFitLineDict[device_name[index]][0],
            rssi_median[device_id[index]],
            bestFitLineDict[device_name[index]][1],
        )

        # value goes to 1 decimal place
        distanceDict[device_name[index]].append(round(predicted_distance, 1))

    return distanceDict


def getRadiusOfBeacons(chosen_devices, chosen_device_names, bestFitLineDict):
    fileName = "predictedValues_data.csv"
    output.writeTitles()
    radiusDict = {}
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        #degrees, testing_values = inputs.askForDistances()

        #for counter in range(len(chosen_devices)):
        #    print("Now testing: " + chosen_device_names[counter])
        #for k in range(1):
            #actual_distance = input(
            #    "What distance are you at right now (for " + chosen_device_names[counter] + "): ")

        distanceDict = collectDataSamples(
            bestFitLineDict, chosen_device_names, chosen_devices
        )
        output.printAndWriteData(
            distanceDict, writer, '0', '0')

        for device in chosen_device_names:
          radiusDict[device] = bestFitCalcs.getAverageDistance(
            distanceDict[device])

    return radiusDict

def withinBounds(bounds, actualCoord):
    actual_x = actualCoord[0]
    actual_y = actualCoord[1]

    withinX = actual_x > bounds[0] and actual_x < bounds[2]
    withinY = actual_y > bounds[1] and actual_y < bounds[3]

    printIsBetween(actual_x, bounds[0], bounds[2], withinX, "X")
    printIsBetween(actual_y, bounds[1], bounds[3], withinY, "Y")



def printIsBetween(actualCoord, minBound, maxBound, within, dir):
    if (within):
        print(str(actualCoord) + " is between " + str(minBound) + " and " + str(maxBound) + "; " + dir + "-dir")
    else:
        print(str(actualCoord) + " is not between " + str(minBound) + " and " + str(maxBound) + "; " + dir + "-dir")

def marginOfError(predictedCoords, actualCoords):
    dist_squared = (predictedCoords[0] - actualCoords[0])**2 + (predictedCoords[1] - actualCoords[1])**2
    dist = math.sqrt(dist_squared)
    return math.trunc(dist)

if __name__ == "__main__":
    (
        chosen_devices,
        chosen_device_names,
        device_positions,
        device_spreadsheets,
        actualCoords
    ) = inputs.getAllInputs()

    print(chosen_devices, chosen_device_names,
          device_positions, device_spreadsheets)

    bestFitLineDict = {}
    distanceDict = defaultdict(list)
    for i in range(len(chosen_device_names)):
        # calculates the a, b values for specified device (logarithmic line of best fit)
        bestFitLineDict = bestFitCalcs.getBestFitLine(
            device_spreadsheets[i], chosen_device_names[i], bestFitLineDict
        )

    radiusDict = getRadiusOfBeacons(
        chosen_devices, chosen_device_names, bestFitLineDict)
    print(radiusDict)
    print(device_positions)
    print(chosen_device_names)

    bounds = draw_circle.get_intersection(
        radiusDict, device_positions, chosen_device_names)

    withinBounds(bounds, actualCoords)

    midpointX = bestFitCalcs.midpoint(bounds[0], bounds[2])
    midpointY = bestFitCalcs.midpoint(bounds[1], bounds[3])

    marginOfError = marginOfError((midpointX, midpointY), actualCoords)
    print(str(marginOfError) + " ft off from center of intersection.")

    draw_circle.visualize_circles(
        radiusDict, device_positions, chosen_device_names, actualCoords)
