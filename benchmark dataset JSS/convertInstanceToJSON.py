# coding: utf-8
import csv
import json
import os
import sys
from pprint import pprint

import pandas

Argv = sys.argv
if (len(Argv) < 2):
    sys.stderr.write("Usage: python %s <instance>\n" % Argv[0])
    quit()

Target = Argv[1]

file = open('instances.json', "r")

data = json.load(file)

instance = [inst for inst in data if inst['name'] == Target]
if (len(instance) == 0):
    raise Exception("There is no instance named %s" % Target)

instance = instance[0]

path = os.path.abspath(os.path.join(os.path.dirname(__file__), instance['path']))

optimum = instance['optimum']
instance_name = instance['name']
instance_jobs = instance['jobs']
instance_machines = instance['machines']

if (optimum is None):
    if (instance['bounds'] is None):
        optimum = "nan"
    else:
        optimum = instance['bounds']['lower']

# sys.stdout.write('--instance %s --optimum %s' % (path, optimum))
# print(instance)
# print(path)

file = open(path, 'r')
csvFilename = "%s_J%s_M%s.csv" % (instance_name, instance_jobs, instance_machines)
jsonFilename = "%s_J%s_M%s_MS%s.json" % (instance_name, instance_jobs, instance_machines, optimum)

with (open(csvFilename, 'w', newline='')) as csvFile:
    writer = csv.writer(csvFile)

    lines = file.read().splitlines()

    for line in lines[5:]:
        line = line.replace("  ", " ").split(" ")
        writer.writerow(line)

jsonData = {}
jsonData["config"] = {"generations": 1000,
                      "popSize": 8}

jsonData["buckets"] = []
jsonData["buckets"].append({"bucketID": 0,
                            "jobs": []})

operationID = 0;
df = pandas.read_csv(csvFilename, dtype=int, header=None)
for idx, row in enumerate(df.iterrows()):
    machine = row[1].iloc[::2]
    duration = row[1].iloc[1::2]

    # print(machine.tolist())
    # print(duration.tolist())
    machineList = machine.tolist()
    jobJSON = {"jobID": idx, "operations": []}
    # jsonData["buckets"][0]["jobs"].append({"jobID":idx, "operations":[]})

    for idx, (mach, dur) in enumerate(zip(machine.tolist(), duration.tolist())):
        jobJSON["operations"].append({
            "operationSequence": idx,
            "process": mach,
            "duration": dur,
            "operationID": operationID
        })
        operationID = operationID + 1;

    jsonData["buckets"][0]["jobs"].append(jobJSON)

# mylist = []

jsonData["processes"] = []
for machine in range(instance_machines):
    jsonData["processes"].append({"processID": machine, "eligibleMachines": [machine], "mappable": True})

jsonData["machines"] = []
for machine in range(instance_machines):
    jsonData["machines"].append({"machineID": machine, "machineFreeTime": 0})

# pprint(jsonData)

with open(jsonFilename, 'w') as outfile:
    json.dump(jsonData, outfile, indent=2, separators=(',', ': '))

os.remove(csvFilename)
sys.stdout.write(
    '--instance %s --optimum %s --jobs %s --machines %s' % (path, optimum, instance_jobs, instance_machines))
