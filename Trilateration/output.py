import Trilateration.bestFitCalcs as bestFitCalcs
import csv


def printData(distanceDict, key, value):

    print("Predicted distance for " + key + ": " + str(value) + " ft")
    print("Average of this collection: " +
          str(bestFitCalcs.getAverageDistance(value)))
    value.sort()
    print("Lowest: " + str(bestFitCalcs.getLowest(value)))
    print("Highest: " + str(bestFitCalcs.getHighest(value)))


def writeDataToOutfile(writer, actual_distance, degrees, key, value):

    writer.writerow(
        [
            actual_distance + " (" + key + ", @" + degrees + " degrees)",
            value,
            bestFitCalcs.getAverageDistance(value),
            (bestFitCalcs.getLowest(value), bestFitCalcs.getHighest(value)),
        ]
    )


def printAndWriteData(distanceDict, writer, actual_distance, degrees):
    for (key, value) in distanceDict.items():
        printData(distanceDict, key, value)
        writeDataToOutfile(writer, actual_distance, degrees, key, value)


def writeTitles():
    fileName = "predictedValues_data.csv"
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(
            [
                "Actual Distance (ft)",
                "Sample Values",
                "Average Predicted Value",
                "Range of Predicted Distances",
            ]
        )
