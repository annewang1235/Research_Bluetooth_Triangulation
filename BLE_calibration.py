import subprocess
import json
import time
import math 

def getDeviceID():
  output = subprocess.check_output("blueutil --format json --paired", shell=True)
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

  chosen = input("Device #: ")
  return (device_arr[int(chosen)], device_name_arr[int(chosen)])

def calibrate(device_id, distance):
  input(f"Move the beacon {distance} meter(s) away\nPress enter to continue...")
  print("Continuing...")
  while(True):
    return getMedian(getRSSISamples(50, device_id))

def getRSSISamples(num_samples, device_id):
  iter_num = 0
  samples = []
  subprocess.check_output("blueutil --connect " + device_id, shell=True)
  while iter_num < num_samples:
    output = subprocess.check_output("blueutil --format json --info " + device_id, shell=True)

    output_json = output.decode("utf-8").replace("'", '"')

    data = json.loads(output_json)

    if data["connected"]:
      samples.append(data["rawRSSI"])
    else:
      print("disconnected. trying to reconnect.")
      subprocess.check_output("blueutil --connect " + device_id, shell=True)
      print("connected...continuing data collection")
      iter_num -= 1
    time.sleep(0.1)
    iter_num += 1
  return sorted(samples)

def getMedian(samples):
  if len(samples) % 2:
    return samples[len(samples) // 2]
  return (samples[(int(len(samples) / 2))] + samples[(int(len(samples) / 2)) - 1]) / 2

def rssi_to_dist(measured_power, envir_const, rssi):
	return 10**((measured_power-rssi)/(10*envir_const))

def calc_envir_const(measured_power):
  envir_const_arr = []
  distance = 2
  for rssi in measured_power[1:]:
    envir_const_arr.append((measured_power[0]-rssi)/(10*math.log(distance, 10)))
    distance += 1
  return getMedian(sorted(envir_const_arr))

if __name__ == "__main__":
  device_id, device_name = getDeviceID()
  measured_power = [calibrate(device_id, x+1) for x in range(3)] # measured_power is the RSSI at various distances
  envir_const = calc_envir_const(measured_power) # an environmental constant from surroundings
  print("Environmental Constant:", envir_const)
  input("Move the Beacon\nPress enter to continue...")
  print("Continuing...")
  samples = getRSSISamples(50, device_id)
  median = getMedian(samples)
  print("Estimated Distance:", rssi_to_dist(measured_power[0], envir_const, median))
