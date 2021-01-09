import Trilateration.inputs as inputs
import Trilateration.bestFitCalcs as bestFitCalcs
import bluetooth_devices
from collections import defaultdict

import csv

import os

if __name__ == "__main__":
    allDeviceAddresses, allDeviceNames = inputs.printsAllDevices()

    chosen_devices, chosen_device_names = inputs.inputChosenDevices(
        allDeviceAddresses, allDeviceNames
    )

    device_positions = inputs.inputPositions(chosen_device_names)
    device_spreadsheets = inputs.inputSpreadsheets(chosen_device_names)

    print(chosen_devices, chosen_device_names, device_positions, device_spreadsheets)

    bestFitLineDict = {}
    distanceDict = defaultdict(list)
    for i in range(len(chosen_device_names)):
        # calculates the m, b values for specified device
        bestFitLineDict = bestFitCalcs.getBestFitLine(
            device_spreadsheets[i], chosen_device_names[i], bestFitLineDict
        )

    # gets 20 predicted distances
    fileName = "predictedValues_data"
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if os.stat(fileName).st_size == 0:
            writer.writerow(
                [
                    "Actual Distance (ft)",
                    "Sample Values",
                    "Average Predicted Value",
                    "Range of Predicted Distances",
                ]
            )
        testing_values = input("How many distances do you want to test: ")
        for k in range(int(testing_values)):

            actual_distance = input("What distance are you at right now: ")
            for j in range(20):
                # gets the RSSI data from specified device
                samples, raw_samples = bluetooth_devices.getRSSISamples(
                    50, chosen_device_names[i]
                )

                # gets the RSSI mode and distance between receiver & i's device
                rssi_median = bluetooth_devices.getMedian(raw_samples)
                print("rssi_mode is " + str(rssi_median))

                predicted_distance = bestFitCalcs.getDistance(
                    bestFitLineDict[chosen_device_names[i]][0],
                    rssi_median,
                    bestFitLineDict[chosen_device_names[i]][1],
                )

                # value goes to 1 decimal place
                distanceDict[chosen_device_names[i]].append(
                    round(predicted_distance, 1)
                )

            for (key, value) in distanceDict.items():
                print("Predicted distance for " + key + ": " + str(value) + " ft")
                print(
                    "Average of this collection: "
                    + str(bestFitCalcs.getAverageDistance(value))
                )
                value.sort()
                print("Lowest: " + str(bestFitCalcs.getLowest(value)))
                print("Highest: " + str(bestFitCalcs.getHighest(value)))

                writer.writerow(
                    [
                        actual_distance,
                        value,
                        bestFitCalcs.getAverageDistance(value),
                        (bestFitCalcs.getLowest(value), bestFitCalcs.getHighest(value)),
                    ]
                )
            distanceDict.clear()
