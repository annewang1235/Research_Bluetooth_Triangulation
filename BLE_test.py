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

  first_pass = getRSSISamples(50, device_id)
  second_pass = getRSSISamples(50, device_id)
  min_pass = getNarrowRange(first_pass, second_pass)
  print(f"Range of RSSI: {getRange(min_pass)}")

  while(True):
    return getMedian(min_pass)

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

def getRange(samples):
  return (samples[0], samples[len(samples) - 1])

def getNarrowRange(first_list, second_list):
  firstRange = getRange(first_list)
  secondRange = getRange(second_list)
  if(firstRange[1]-firstRange[0] < secondRange[1]-secondRange[0]):
    return first_list
  return second_list

def rssi_to_dist(measured_power, envir_const, rssi):
  # initial guess based off median environmental const of samples
  my_envir_const = getMedian(sorted(envir_const))

  dist_guess = 10**((measured_power-rssi)/(10*my_envir_const))
  envir_index = int(dist_guess)-1
  
  if(envir_index >= len(envir_const)-1):
    return 10**((measured_power-rssi)/(10*envir_const[len(envir_const)-1]))
  elif(envir_index < len(envir_const)/2):
    return 10**((measured_power-rssi)/(10*envir_const[envir_index]))
  return dist_guess
	

def calc_envir_const(measured_power):
  envir_const_arr = []
  distance = 2
  for rssi in measured_power[1:]:
    envir_const_arr.append((measured_power[0]-rssi)/(10*math.log(distance, 10)))
    distance += 1
  return envir_const_arr

# Printing the Grid Layout
def print_grid(n, grid_values):
    print()
    print("\t\t\tTrilateration Grid\n")
 
    st = "   "
    for i in range(n):
        st = st + "     " + str(i)
    print(st)   
 
    for r in range(n):
        st = "     "
        if r == 0:
            for col in range(n):
                st = st + "______" 
            print(st)
 
        st = "     "
        for col in range(n):
            st = st + "|     "
        print(st + "|")
         
        st = "  " + str(r) + "  "
        for col in range(n):
            st = st + "|  " + str(grid_values[r][col]) + "  "
        print(st + "|") 
 
        st = "     "
        for col in range(n):
            st = st + "|_____"
        print(st + '|')
 
    print()

if __name__ == "__main__":
  
  device_id_1, device_name_1 = getDeviceID()
  device_id_2, device_name_2 = getDeviceID()
  
  print("Calibration for First Beacon")
  measured_power_1 = [calibrate(device_id_1, x+1) for x in range(5)] # measured_power is the RSSI at various distances
  envir_const_1 = calc_envir_const(measured_power_1) # an environmental constant from surroundings
  print(" env_const1 = [", end="")
  for val in envir_const_1[:-1]:
    print(f"{val:.2f}, ", end="")
  print(f"{envir_const_1[-1]:.2f}]")

  print("Calibration for Second Beacon")
  measured_power_2 = [calibrate(device_id_2, x+1) for x in range(5)] # measured_power is the RSSI at various distances
  envir_const_2 = calc_envir_const(measured_power_2) # an environmental constant from surroundings
  print(" env_const2 = [", end="")
  for val in envir_const_2[:-1]:
    print(f"{val:.2f}, ", end="")
  print(f"{envir_const_2[-1]:.2f}]")

  run = 1
  while("q" != input("Move the Beacon\nPress enter to continue(or Q to exit)...").lower()):
    print(f"Continuing With Test #{run}...")
    samples_1 = getRSSISamples(50, device_id_1)
    samples_2 = getRSSISamples(50, device_id_2)
    
    print(f"Range of RSSI 1: {getRange(samples_1)}")
    median_1 = getMedian(samples_1)

    print(f"Range of RSSI 2: {getRange(samples_2)}")
    median_2 = getMedian(samples_2)
    
    appr_dist_1 = rssi_to_dist(measured_power_1[0], envir_const_1, median_1)
    print(f"Estimated Distance 1: {appr_dist_1:.2f}")
    
    appr_dist_2 = rssi_to_dist(measured_power_2[0], envir_const_2, median_2)
    print(f"Estimated Distance 2: {appr_dist_2:.2f}")
  
    # n = 10 if int(appr_dist)+2 < 10 else int(appr_dist)+2
    # grid_values = [[" " for x in range(n)] for y in range(n)]
    # grid_values[0][0] = "B"
    # grid_values[0][int(appr_dist)] = "H"
    # print_grid(n, grid_values)
    run += 1

