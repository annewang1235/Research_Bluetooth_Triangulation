import subprocess
import json
from collections import defaultdict


def distanceStrength(distanceToStrength):

    output = subprocess.check_output("blueutil --format json --paired", shell=True)

    output_json = output.decode("utf-8").replace(
        "'", '"'
    )  # decodes the byte into a json

    data = json.loads(output_json)  # loads the json into a dictionary

    ele = data[0]
    if ele["connected"]:
        print(ele["name"], " ==> Signal strength: ", ele["RSSI"])

        distanceToStrength[distance].append(ele["RSSI"])

    else:
        print(ele["name"], " is not connected.")

    print(distanceToStrength)


if __name__ == "__main__":
    distanceToStrength = defaultdict(list)
    for i in range(3):
        distance = input("Enter your distance: ")
        distanceStrength(distanceToStrength)
