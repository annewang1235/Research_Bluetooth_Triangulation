import numpy as np
import matplotlib.pyplot as plt
import pylab

import math


def getBestFitLine(fileName, device_name, bestFitLineDict):
    with open(fileName) as f:
        next(f)
        data = [[line.split(",")[0], line.split(",")[1]]
                for line in f.readlines()]

        x_vals = np.array([float(x) for x, y in data])
        y_vals = np.array([float(y) for x, y in data])

        plotData(x_vals, y_vals, data)

        # m, b = np.polyfit(x_vals, y_vals, 1)
        a, b = np.polyfit(np.log(x_vals), y_vals, 1)

        # device_name is the key
        bestFitLineDict[device_name] = (a, b)

        print(bestFitLineDict)
        return bestFitLineDict


def plotData(x_vals, y_vals, data):
    plt.clf()
    for (x, y) in data:
        plt.scatter(float(x), float(y))

    plt.xlabel("Distance (ft)")
    plt.ylabel("RSSI Values")
    plt.title("Distance Vs RSSI Values")

    a, b = np.polyfit(np.log(x_vals), y_vals, 1)
    # print(a, b)

    x = np.arange(0.1, 20, 0.1)
    plt.plot(x, a * np.log(x) + b)
    
    plt.ion()
    plt.show()
    plt.pause(0.001)
    input("Press enter to continue...")
    #plt.close()

def getDistance(a, rssi, b):
    return np.exp((rssi - b) / a)


def getAverageDistance(predictedDistances: list):
    sum = 0
    for element in predictedDistances:
        sum += element

    return round(sum / len(predictedDistances), 1)


def getLowest(predictedDistances: list):
    return predictedDistances[0]


def getHighest(predictedDistances: list):
    return predictedDistances[len(predictedDistances) - 1]


def _getMidpoint(minBound, maxBound):
    return (minBound + maxBound)/2.0


def _getMarginOfError(predictedCoords, actualCoords):
    dist_squared = (predictedCoords[0] - actualCoords[0])**2 + (predictedCoords[1] - actualCoords[1])**2
    dist = math.sqrt(dist_squared)
    return round(dist, 2)

def getIntersectionCenter(intersection, actualCoords):
    if (intersection == None ):
        print("No intersection")
        return

    minX, minY, maxX, maxY = intersection.bounds

    midpointX = _getMidpoint(minX, maxX)
    midpointY = _getMidpoint(minY, maxY)

    marginOfError = _getMarginOfError((midpointX, midpointY), actualCoords)
    print(str(marginOfError) + " ft off from center of intersection.")


