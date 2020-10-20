import subprocess
import json

output = subprocess.check_output("blueutil --format json --paired", shell=True)

output_json = output.decode("utf-8").replace("'", '"')  # decodes the byte into a json

print()
data = json.loads(output_json)  # loads the json into a dictionary

for ele in data:
    print(ele["name"], " ==> Signal strength: ", ele["RSSI"])
    # testing some pull request thing out
