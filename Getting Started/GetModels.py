import json
import os
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
RECORDCOUNT = 3
STARTINDEX = 0

try:
    #Delete if file already exists
    if os.path.exists(CSVPATH):
        os.remove(CSVPATH)
    
    #Get All records from
    print("Retrieving Models")    
    customFieldCount = 0
    csvFinalData = ''
    csvHeader = "Model_id,Model_referenceId,Model_shortName,Model_name,Model_notes,Model_itemTypePath,Model_importance,Model_strategy,Model_uom,Model_replacementCost,"\
                "Model_economicLife,Model_designLife,Model_lifeFactor,Model_status,Model_conditionDescriptor,Model_baseRegion,Model_uniqueIdentifier,Model_profile,"\
                "Task_id,Task_referenceId,Task_name,Task_shortName,Task_originalCost,Task_uom,Task_importance,Task_costFactor,Task_uniqueIdentifier,"\
                "Resource_id,Resource_referenceId,Resource_name,Resource_shortName,Resource_type,Resource_uom,Resource_quantity,Resource_defaultCost,Resource_uniqueIdentifier,"\
                "Resource_costBPILoadDate,Costs_region,Costs_amount,Costs_currency\r"

    print('Retrieving records: ',str(STARTINDEX),"-",str((STARTINDEX + RECORDCOUNT-1)))
    PARAMS = {'count': RECORDCOUNT,'startIndex': STARTINDEX}
    responseModels = pip._vendor.requests.get(url = MODELURL, params = PARAMS, headers = HEADERS)
    models = responseModels.json()
    csvData = ''
        
    #Transformation for CSV generation
    #Data records
    print('Transforming records')
    for model in models["data"]:
        for task in model['tasks']:
            for resource in task['resources']:
                for cost in resource['costs']:
                    #Print all model fields
                    csvData = csvData + '"' + str(model['id']) + '","' + str(model['referenceId'] or '') + '","' + str(model['shortName'] or '') + '","' + str(model['name'] or '') + '","' + str(model['notes'] or '')
                    csvData = csvData + '","' + str(model['itemTypePath'] or '') + '","' + str(model['importance'] or '') + '","' + str(model['strategy'] or '') + '","' + str(model['uom'] or '') + '","' + str(model['replacementCost'] or '') + '","' + str(model['economicLife'] or '')
                    csvData = csvData + '","' + str(model['designLife'] or '') + '","' + str(model['lifeFactor'] or '') + '","' + str(model['status'] or '') + '","' + str(model['conditionDescriptor'] or '') + '","' + str(model['baseRegion'] or '') + '","' + str(model['uniqueIdentifier'] or '')
                    csvData = csvData + '","' + str(model['profile'] or '')
                    #Task fields
                    csvData = csvData + '","' + str(task['id'] or '') + '","' + str(task['referenceId'] or '') + '","' + str(task['name'] or '') + '","' + str(task['shortName'] or '') + '","' + str(task['originalCost'] or '')
                    csvData = csvData + '","' + str(task['uom'] or '') + '","' + str(task['importance'] or '') + '","' + str(task['costFactor'] or '') + '","' + str(task['uniqueIdentifier'] or '')
                    #Resource fields
                    csvData = csvData + '","' + str(resource['id']) + '","' + str(resource['referenceId'] or '') + '","' + str(resource['name'] or '') + '","' + str(resource['shortName'] or '')
                    csvData = csvData + '","' + resource['type'] + '","' + str(resource['uom'] or '') + '","' + str(resource['quantity'] or '') + '","' + str(resource['defaultCost'] or '')
                    csvData = csvData + '","' + str(resource['uniqueIdentifier'] or '') + '","' + str(resource['costBPILoadDate'] or '')
                    #Cost fields
                    csvData = csvData + '","' + cost['region'] + '","' + str(cost['amount'] or '') + '","' + str(cost['currency'] or '') + '"' + "\r"
        
    csvFinalData = csvFinalData + csvData    

    with open(CSVPATH, 'a') as data_out :
        data_out.write(csvHeader + csvFinalData)        
    print('CSV generated at ' + CSVPATH)

except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))