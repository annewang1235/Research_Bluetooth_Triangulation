import subprocess
import json
import time

def getRSSISamples(num_samples, distance):
    iter_num = 0
    samples = []
    raw_samples = []
    while(iter_num < num_samples):
        output = subprocess.check_output("blueutil --format json --paired", shell=True)

        output_json = output.decode("utf-8").replace("'", '"')

        data = json.loads(output_json)

        for ele in data:
            if(ele["connected"]):
                samples.append(ele["RSSI"])
                raw_samples.append(ele["rawRSSI"])
                print("Iteration Count: "+str(iter_num+1))
        time.sleep(0.1)
        iter_num += 1
    return (sorted(samples), sorted(raw_samples))

def getMean(samples):
    sum = 0
    for sample in samples:
        sum += sample
    return sum/len(samples)
    
def getMedian(samples):
    if(len(samples)%2):
        return samples[len(samples)/2]
    return (samples[(int(len(samples)/2))] + samples[(int(len(samples)/2))-1])/2
    
def getRange(samples):
    return (samples[0], samples[len(samples)-1])
    
def getMode(samples):
    return max(set(samples), key=samples.count)

if __name__ == '__main__':
    distance = input("Distance from beacon: ")
    samples = getRSSISamples(100, distance)
    range = getRange(samples[0])
    raw_range = getRange(samples[1])
    
    print()
    print("RSSI Stats")
    print("RANGE:", getRange(samples[0]))
    print("MEAN:", getMean(samples[0]))
    print("MEDIAN:", getMedian(samples[0]))
    print("MODE:", getMode(samples[0]))
    print()
    
    print("rawRSSI Stats")
    print("RANGE:", getRange(samples[1]))
    print("MEAN:", getMean(samples[1]))
    print("MEDIAN:", getMedian(samples[1]))
    print("MODE:", getMode(samples[1]))
    
