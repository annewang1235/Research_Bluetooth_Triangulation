import Trilateration.inputs as inputs
import Trilateration.bestFitCalcs as bestFitCalcs
import Trilateration.output as output
import bluetooth_devices
from collections import defaultdict


import csv

import os


def collectDataSamples(bestFitLineDict, device_name, device_id):
    for j in range(20):
        # gets the RSSI data from specified device
        samples, raw_samples = bluetooth_devices.getRSSISamples(50, device_id)

        # gets the RSSI mode and distance between receiver & i's device
        rssi_median = bluetooth_devices.getMedian(raw_samples)
        print("rssi_mode is " + str(rssi_median))

        predicted_distance = bestFitCalcs.getDistance(
            bestFitLineDict[device_name][0],
            rssi_median,
            bestFitLineDict[device_name][1],
        )

        # value goes to 1 decimal place
        distanceDict[device_name].append(round(predicted_distance, 1))

    return distanceDict


if __name__ == "__main__":
    (
        chosen_devices,
        chosen_device_names,
        device_positions,
        device_spreadsheets,
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

    fileName = "predictedValues_data.csv"
    output.writeTitles()
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        degrees, testing_values = inputs.askForDistances()

        for counter in range(len(chosen_devices)):
            for k in range(int(testing_values)):
                actual_distance = input("What distance are you at right now: ")

                distanceDict = collectDataSamples(
                    bestFitLineDict, chosen_device_names[counter], chosen_devices[counter]
                )
                output.printAndWriteData(
                    distanceDict, writer, actual_distance, degrees)

                distanceDict.clear()
