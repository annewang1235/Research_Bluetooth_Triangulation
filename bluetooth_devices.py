import subprocess
import json
import time

if __name__ == '__main__':
    while(True):
        output = subprocess.check_output("blueutil --format json --paired", shell=True)

        output_json = output.decode("utf-8").replace("'", '"')

        data = json.loads(output_json)
        # print(data)
        # print(type(data))

        for ele in data:
            if("rawRSSI" in ele):
                print(ele["name"] +" Signal Strength: "+str(ele["rawRSSI"]))
        time.sleep(0.5)

