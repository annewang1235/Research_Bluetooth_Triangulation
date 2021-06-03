import subprocess
import json
import time

import csv

import os

import asyncio
import platform

from bleak import BleakClient, BleakScanner
from bleak.backends.corebluetooth.client import BleakClientCoreBluetooth
from bleak.backends.device import BLEDevice

async def getDeviceID():
  scanner = BleakScanner()
  await scanner.start()
  await asyncio.sleep(10.0)
  await scanner.stop()
  devices = await scanner.get_discovered_devices()
  index = 0
  for d in devices:
    print(index, d.name)
    index += 1

  chosen = input("Device #: ")
  return (devices[int(chosen)].address, devices[int(chosen)].name)

# device_map maps the addresses to names
async def getRSSISamples(num_samples, device_id, device_map):
    device = BleakClientCoreBluetooth(device_id, timeout=20.0)
    await device.connect()
    iter_num = 0
    raw_arr = []
    
    while iter_num < num_samples:
      if device.is_connected:
        raw_arr.append(await device.get_rssi())
        print(device_map[device_id], "Iteration Count:", iter_num + 1)
      else:
        print("disconnected. trying to reconnect.")
        await device.connect()        
        print("connected...continuing data collection")
        # last sample is outlier if disconnected so we remove it
        raw_arr.pop()
        iter_num -= 1

      await asyncio.sleep(0.1)
      iter_num += 1
    
    raw_arr.sort()
    return raw_arr


def getMean(samples):
    sum = 0
    for sample in samples:
        sum += sample
    return sum / len(samples)


def getMedian(samples):
    if len(samples) % 2:
        return samples[len(samples) // 2]
    return (samples[(int(len(samples) / 2))] + samples[(int(len(samples) / 2)) - 1]) / 2


def getRange(samples):
    return (samples[0], samples[len(samples) - 1])


def getMode(samples):
    return max(set(samples), key=samples.count)


def printData(distance, rangeOfRSSI, mean, median, mode):
    print()
    print("rawRSSI Stats For", distance, "Feet Away")
    print("RANGE:", rangeOfRSSI)
    print("MEAN:", mean)
    print("MEDIAN:", median)
    print("MODE:", mode)
    print()

async def run():
  device_id, device_name = await getDeviceID()
  device_dict = dict()
  device_dict[device_id] = device_name
  startVal = 1
  endVal = 20

  fileName = "bluetooth_data_" + device_name + ".csv"

  # each device has its own specific spreadsheet, name of spreadsheet to include name of device
  with open(fileName, "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    if os.stat(fileName).st_size == 0:
      writer.writerow(
        ["Distance (ft)", "Raw RSSI Median", "Range of RSSI", "Mean"]
      )

    for i in range(startVal, endVal + 1):
      distance = input(f'{i} feet away from Beacon\npress enter to continue...')
      samples = await getRSSISamples(100, device_id, device_dict)

      # raw RSSI ranges
      raw_range = getRange(samples)

      # raw RSSI mean, median, mode
      raw_mean = getMean(samples)
      raw_median = getMedian(samples)
      raw_mode = getMode(samples)
      printData(i, raw_range, raw_mean, raw_median, raw_mode)

      writer.writerow([i, raw_median, raw_range, raw_mean])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())    
    
    