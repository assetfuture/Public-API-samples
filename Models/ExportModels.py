import json
import os
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
RECORDCOUNT = 1000
STARTINDEX = 0

modelCount = RECORDCOUNT
try:
    #Delete if file already exists
    if os.path.exists(CSVPATH):
        os.remove(CSVPATH)
    
    #Get All records from
    print("Retrieving Models")    
    customFieldCount = 0
    csvFinalData = ''
    csvHeader = "ModelId,ModelName,TaskId,TaskName,ResourceId,ResourceName,Region,Amount,Currency\r"
    while modelCount >= RECORDCOUNT:
        print('Retrieving records: ',str(STARTINDEX),"-",str((STARTINDEX + RECORDCOUNT-1)))
        PARAMS = {'count': RECORDCOUNT,'startIndex': STARTINDEX}
        responseModels = pip._vendor.requests.get(url = MODELURL, params = PARAMS, headers = HEADERS)
        models = responseModels.json()
        STARTINDEX = STARTINDEX + RECORDCOUNT
        modelCount = models["count"]
        csvData = ''
        
        #Transformation for CSV generation
        #Data records
        print('Transforming records')
        for model in models["data"]: 
            for task in model['tasks']:
                for resource in task['resources']:
                    for cost in resource['costs']:
                        csvData = csvData + str(model['dbId']) + ',"' + model['name'] + '",' + str(task['dbId']) + ',"' + task['name'] +'"'
                        csvData = csvData + ',' + str(resource['dbId']) + ',"' + resource['name'] + '",' + cost['region']
                        csvData = csvData + ',' + str(cost['amount'] or '') + ',' + str(cost['currency'] or '') + "\r"
        
        csvFinalData = csvFinalData + csvData    

    with open(CSVPATH, 'a') as data_out :
        data_out.write(csvHeader + csvFinalData)        
    print('CSV generated at ' + CSVPATH)

except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))