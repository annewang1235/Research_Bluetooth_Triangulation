# This file is so manage all the inputs for the program.
import subprocess
import json
import glob


def printsAllDevices():
    output = subprocess.check_output(
        "blueutil --format json --paired", shell=True)

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

    return (device_arr, device_name_arr)


def inputChosenDevices(device_arr, device_name_arr):
    chosen_indexes = input("Device #'s (separated by a space): ").split()

    chosen_devices = []
    chosen_device_names = []
    for index in chosen_indexes:
        chosen_devices.append(device_arr[int(index)])
        chosen_device_names.append(device_name_arr[int(index)])

    return (chosen_devices, chosen_device_names)


def inputPositions(chosen_device_names):
    print("Use a space to separate x and y coordinates")

    positions = []
    for device in chosen_device_names:
        x, y = input("Position for " + device + ": ").split()
        positions.append((float(x), float(y)))

    return positions


def inputSpreadsheets(chosen_device_names):
    choices = glob.glob("*/*.{}".format('csv')) #this accts for all csv files, in case we switch between Arduinos and RPis
    spreadsheets = []
    index = 0
    for ele in choices:
        print(index, ele)
        index += 1

    for device in chosen_device_names:
        data = input("Spreadsheet # for " + device + ": ")
        spreadsheets.append(choices[int(data)])
    return spreadsheets

def inputActualCoords():

    x, y = input("Actual Position of receiver?: ").split()
    return (float(x), float(y))

   

def askForDistances():
    degrees = input("At what degree of the bluetooth are you testing: ")
    testing_values = input("How many distances do you want to test: ")

    return (degrees, testing_values)



def getAllInputs():
    allDeviceAddresses, allDeviceNames = printsAllDevices()

    chosen_devices, chosen_device_names = inputChosenDevices(
        allDeviceAddresses, allDeviceNames
    )

    # device_positions = inputPositions(chosen_device_names)
    device_spreadsheets = inputSpreadsheets(chosen_device_names)
    actualCoords = inputActualCoords()

    return (
        chosen_devices,
        chosen_device_names,
        # device_positions,
        device_spreadsheets,
        actualCoords
    )
