import Trilateration.inputs as inputs
import Trilateration.bestFitCalcs as bestFitCalcs
import bluetooth_devices

if __name__ == "__main__":
    allDeviceNames = ["HC_01", "HC_02", "HC_03", "HC_04", "HC_05", "HC_06"]
    allDeviceAddresses = ["addy 1", "addy 2", "addy 3", "addy 4", "addy 5", "addy 6"]

    chosen_devices, chosen_device_names = inputs.inputChosenDevices(
        allDeviceAddresses, allDeviceNames
    )

    device_positions = inputs.inputPositions(chosen_device_names)
    device_spreadsheets = inputs.inputSpreadsheets(chosen_device_names)

    print(chosen_devices, chosen_device_names, device_positions, device_spreadsheets)

    # pseudo code
    # gets data from spreadsheets and calculates the m, b
    # gets the data samplese from each bluetooth and calculates the distance
    bestFitLineDict = {}
    distanceDict = {}
    for i in range(len(chosen_device_names)):
        bestFitLineDict = bestFitCalcs.getBestFitLine(
            device_spreadsheets[i], chosen_device_names[i], bestFitLineDict
        )

        samples, raw_samples = bluetooth_devices.getRSSISamples(
            100, chosen_device_names[i]
        )

        # gets the RSSI mode and distance between receiver & i's device
        rssi_mode = bluetooth_devices.getMode(raw_samples)
        distanceDict[chosen_device_names[i]] = rssi_mode

    for (key, value) in distanceDict:
        print("Predicted distance for " + key + ": " + value + " ft")
