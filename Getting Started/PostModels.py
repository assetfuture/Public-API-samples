import json
import csv
import pip._vendor.requests

#Replace with your api subscription key.
#Generated after signing-up to the developer portal.
#To retrieve subscription key, sign-in to developer portal and access "Try it" section for any API
KEY = 'subscription-key'

#Replace with path for generating the CSV file
CSVPATH = ".\\Filename.csv"

#API urls that needs to be accessed
MODELURL = "https://api.assetfuture.com/model/Models"

HEADERS = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': KEY}

jsonArray = []

#read csv file
with open(CSVPATH, encoding='utf-8') as csvf: 
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
        costDict["region"] = row['Costs_region']
        costDict["amount"] = row['Costs_amount']
        costDict["currency"] = row['Costs_currency']
        costArray.append(costDict)
        resourceDict["id"] = row['Resource_id']
        resourceDict["costBPILoadDate"] = row['Resource_costBPILoadDate']
        resourceDict["uniqueIdentifier"] = row['Resource_uniqueIdentifier']
        resourceDict["quantity"] = row['Resource_quantity']
        resourceDict["uom"] = row['Resource_uom']
        resourceDict["type"] = row['Resource_type']
        resourceDict["shortName"] = row['Resource_shortName']
        resourceDict["name"] = row['Resource_name']
        resourceDict["referenceId"] = row['Resource_referenceId']
        resourceDict["costs"] = costArray
        resourceArray.append(resourceDict)
        taskDict["id"] = row['Task_id']
        taskDict["name"] = row['Task_name']
        taskDict["shortName"] = row['Task_shortName']
        taskDict["referenceId"] = row['Task_referenceId']
        taskDict["originalCost"] = row['Task_originalCost']
        taskDict["uom"] = row['Task_uom']
        taskDict["importance"] = row['Task_importance']
        taskDict["uniqueIdentifier"] = row['Task_uniqueIdentifier']
        taskDict["resources"] = resourceArray
        taskArray.append(taskDict)
        modelDict["id"] = row['Model_id']
        modelDict["referenceId"] = row['Model_referenceId']
        modelDict["shortName"] = row['Model_shortName']
        modelDict["name"] = row['Model_name']
        modelDict["notes"] = row['Model_notes']
        modelDict["itemTypePath"] = row['Model_itemTypePath']
        modelDict["importance"] = row['Model_importance']
        modelDict["strategy"] = row['Model_strategy']
        modelDict["uom"] = row['Model_uom']
        modelDict["replacementCost"] = row['Model_replacementCost']
        modelDict["economicLife"] = row['Model_economicLife']
        modelDict["designLife"] = row['Model_designLife']
        modelDict["lifeFactor"] = row['Model_lifeFactor']
        modelDict["status"] = row['Model_status']
        modelDict["conditionDescriptor"] = row['Model_conditionDescriptor']
        modelDict["baseRegion"] = row['Model_baseRegion']
        modelDict["uniqueIdentifier"] = row['Model_uniqueIdentifier']
        modelDict["profile"] = row['Model_profile']
        modelDict["tasks"] = taskArray
        jsonArray.append(modelDict)
        responseItems = pip._vendor.requests.post(url = MODELURL, json=jsonArray, headers = HEADERS)
        response = responseItems.json()
        print (response)
    