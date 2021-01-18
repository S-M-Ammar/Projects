import json
from pprint import pprint

outputData = {
    "generations": 5000,
    "popSize": 8,
    "scheduleStartTime": "2020-06-18T08:00:00.000Z",

    "workshop": "52",
    "factory": "AMF",
    "batchSize": 1,

    "fabricationOrders": [],
    "machines": [],
    "processes": []
}

inputFile = "la19_J10_M10_MS842.json"
file = open(inputFile, "r")

data = json.load(file)

# pprint(data["buckets"])

for FO in data["buckets"][0]["jobs"]:

    FOobj = {
        "foId": FO["jobID"],
        "partNumber": str(FO["jobID"]),
        "partName": "Front Stranger",
        "qualityCode": "QC123",
        "QPA": 1,
        "aircraftSection": "Wing",
        "sbgActivity": "Pre-Jig",
        "level": 1,
        "priority": 0,
        "operations": []
    }

    for index, op in enumerate(FO["operations"]):
        FOobj["operations"].append({
            "opId": FO["jobID"] * 10 + index,
            "sequence": op["operationSequence"] * 5,
            "processId": op["process"],
            "machineSetupTime": 0,
            "partSetupTime": 0,
            "operationTime": op["duration"],
            "trade": "electrical",
            "mappable": True

        })

    outputData["fabricationOrders"].append(FOobj)
#
for machine in data["machines"]:
    outputData["machines"].append({
        "machineId": machine["machineID"],
        "machineName": "Machine " + str(machine["machineID"]),
        "machineFreeTime": 0
    })

for process in data["processes"]:
    outputData["processes"].append({
        "processId": process["processID"],
        "processName": str(process["processID"]),
        "processCode": str(process["processID"]),
        "machines": process["eligibleMachines"]
    })

pprint(outputData)

with open("JSSBackendInputData.json", 'w') as outfile:
    json.dump(outputData, outfile, indent=4, separators=(',', ': '))
