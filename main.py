import Trilateration.inputs as inputs
import Trilateration.bestFitCalcs as bestFitCalcs
import bluetooth_devices

if __name__ == "__main__":
    allDeviceAddresses, allDeviceNames = inputs.printsAllDevices()

    chosen_devices, chosen_device_names = inputs.inputChosenDevices(
        allDeviceAddresses, allDeviceNames
    )

    device_positions = inputs.inputPositions(chosen_device_names)
    device_spreadsheets = inputs.inputSpreadsheets(chosen_device_names)

    print(chosen_devices, chosen_device_names, device_positions, device_spreadsheets)

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