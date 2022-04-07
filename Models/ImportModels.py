import json
import csv
import pip._vendor.requests

#Replace with your api subscription key.
#Generated after signing-up to the developer portal.
#To retrieve subscription key, sign-in to developer portal and access "Try it" section for any API
KEY = '<Subscripton-Key>'

#Replace with path for generating the CSV file
CSVPATH = ".\\FileName.csv"

#API urls that needs to be accessed
MODELURL = "https://api.assetfuture.com/model/Models"

HEADERS = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': KEY}

def CsvToJsonArray(csvFilePath):
    jsonArray = []

    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 

        #convert to jsonArray
        for row in csvReader: 
            modelDict = {}
            taskArray = []
            taskDict = {}
            resourceArray = []
            resourceDict = {}
            costArray = []
            costDict = {}
            costDict["region"] = row['Region']
            costDict["amount"] = row['Amount']
            costDict["currency"] = row['Currency']
            costArray.append(costDict)
            resourceDict["dbId"] = row['ResourceId']
            resourceDict["costs"] = costArray
            resourceArray.append(resourceDict)
            taskDict["dbId"] = row['TaskId']
            taskDict["resources"] = resourceArray
            taskArray.append(taskDict)
            modelDict["dbId"] = row['ModelId']
            modelDict["tasks"] = taskArray
            jsonArray.append(modelDict)
        return jsonArray

try:
    data = CsvToJsonArray(CSVPATH)
    print(data)
    responseItems = pip._vendor.requests.put(url = MODELURL, json=data, headers = HEADERS)
    response = responseItems.json()
    print (response)
    
except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))