import json
import os
import requests

#Replace with your api subscription key.
#Generated after signing-up to the developer portal.
#To retrieve subscription key, sign-in to developer portal and access "Try it" section for any API
KEY = '<SUBSCRIPTION-KEY>'

#API urls that needs to be accessed
AREAURL = "https://api.assetfuture.com/inventory/Areas"
ITEMURL = "https://api.assetfuture.com/inventory/Items"

HEADERS = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': KEY}

RECORDCOUNT = 1000
STARTINDEX = 0
CSVPATH = ".\\FileName.csv"
itemCount = RECORDCOUNT
areaCount = RECORDCOUNT
dictAreas = {}
try:
    #Delete if file already exists
    if os.path.exists(CSVPATH):
        os.remove(CSVPATH)
    
    #Get All records from Areas API
    print("Retrieving Areas")
    while areaCount >= RECORDCOUNT:
        PARAMS = {'count': RECORDCOUNT,'startIndex': STARTINDEX}
        print (PARAMS)
        response = requests.get(url = AREAURL, params = PARAMS, headers = HEADERS)
        areas = response.json()
        STARTINDEX = STARTINDEX + RECORDCOUNT
        areaCount = areas["count"]
        for area in areas["data"]: 
            dictAreas[str(area["areaPath"] or '')] = area

    #Get records from Items API
    STARTINDEX = 0
    print("Retrieveing Items")
    csvFinalData = ''    
    csvHeader = "Asset Id,Space code,Area,Space type,Item Type,Item Name,Shortname,ModelId,ModelName,Quantity,Survey Condition,Survey Condition Date,Cost Factor,Life Factor,Duty Factor,"
    csvHeader = csvHeader + "Strategy,Years to replace,Proprietory name,Tracking identifier,Cost per unit,Manufacturer,Model No,Serial No, Supplier name, Supplier contact,"
    csvHeader = csvHeader + "Manufactured date, Installed date, Obsolete date,Notes,Warranty,Replacement condition,Risk name,Unit of measure,Importance"
    
    customFieldCount = 0
    while itemCount >= RECORDCOUNT:
        PARAMS = {'count': RECORDCOUNT,'startIndex': STARTINDEX}
        print (PARAMS)
        responseItems = requests.get(url = ITEMURL, params = PARAMS, headers = HEADERS)
        items = responseItems.json()
        STARTINDEX = STARTINDEX + RECORDCOUNT
        itemCount = items["count"]
        csvData = ''
        #Transformation for CSV generation
        #Data records
        for item in items["data"]: 
            #format area path for extracting area related fields
            if dictAreas.get(item["area"],'') != '':
                spaceCode = str(dictAreas.get(item["area"])["shortName"] or '')
                spaceType = str(dictAreas.get(item["area"])["type"] or '')
            else:
                spaceCode = ''
                spaceType = ''
            csvData = csvData + item["referenceId"] + ","
            csvData = csvData + spaceCode + ","
            csvData = csvData + item["area"] + ","
            csvData = csvData + spaceType + ","
            csvData = csvData + item["typePath"] + ","
            csvData = csvData + '"' + str(item["name"] or '').replace('"','""') + '"' + ","
            csvData = csvData + '"' + str(item["shortName"] or '').replace('"','""') + '"' + ","
            csvData = csvData + '"' + str(item["modelId"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["modelName"] or '').replace('"','""') + '"' + ","
            csvData = csvData + '"' + str(item["quantity"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["surveyCondition"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["surveyConditionDate"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["costFactor"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["lifeFactor"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["dutyFactor"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["strategy"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["yearsToReplace"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["proprietaryName"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["trackingIdentifier"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["costPerUnit"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["manufacturer"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["modelNo"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["serialNo"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["supplierName"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["supplierContact"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["manufacturedDate"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["installedDate"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["obsoleteDate"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["notes"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["warranty"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["replacementCondition"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["riskName"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["unitOfMeasure"] or '') + '"' + ","
            csvData = csvData + '"' + str(item["importance"] or '') + '"'
            i=0
            #transform extensions to columns        
            if len(item["extensions"]) > 0:
                extensions = json.dumps(item["extensions"])

                for exRow in item["extensions"]:
                    i=i+1
                    if exRow["describe"]:
                        csvData = csvData  + "," + exRow["describe"] + "," + str(exRow["valueChar"] or str(exRow["valueInt"] or str(exRow["valueDouble"] or str(exRow["valueBit"] or str(exRow["valueDate"] or '')))))
                    if i > customFieldCount:
                        customFieldCount = i
            csvData = csvData + "\r"
        csvFinalData = csvFinalData + csvData
    
    while customFieldCount > 0:
        csvHeader = csvHeader + ",CustomField,Value"
        customFieldCount =  customFieldCount - 1
    
    csvHeader = csvHeader + "\r"

    with open(CSVPATH, 'a') as data_out :
        data_out.write(csvHeader + csvFinalData)        
    print('CSV generated at ' + CSVPATH)

except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))