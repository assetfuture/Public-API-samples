# Reading an excel file using Python
import sys
import json
import pandas as pd
import requests

#API Parameters
KEY = 'Subscription-key'
TRANSACTIONALSURL = "https://api.assetfuture.com/plans/Transactionals"
HEADERS = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': KEY}

#CSV File
HEADER_ROW_NUM = 1
INDEX = 1
CSV_FILE = ".\\Filename.csv"
COL_ASSETID = ""
COL_MAINTENANCECOST = ""
COL_MAINTENANCEDATE = ""
COL_MAINTENANCETYPE = ""
COL_REPAIRCOST = ""
COL_REPAIRDATE = ""
COL_REPAIRDESCRIPTION = ""
COL_REPLACEMENTDATE = ""
COL_REPLACEMENTCOST = ""
ACTIVITYTYPE_MAINTENANCE = "Maintenance"
ACTIVITYTYPE_REPAIRS = "Repairs"
ACTIVITYTYPE_REPLACEMENT = "Replacement"
JSON_FILE = ".\\filename.json"
DATA_SHEET = 'Sheet name'
jsonArray = []
try:

    print(len(sys.argv))

    #Read data from excel
    data = pd.read_excel (CSV_FILE, sheet_name=DATA_SHEET,header = HEADER_ROW_NUM)

    
    df = pd.DataFrame(data, columns= [COL_ASSETID,COL_MAINTENANCECOST,COL_MAINTENANCEDATE,
    COL_MAINTENANCETYPE,COL_REPAIRCOST,COL_REPAIRDATE,COL_REPAIRDESCRIPTION,
    COL_REPLACEMENTDATE,COL_REPLACEMENTCOST])
    

    if(sys.argv[1].lower() == ACTIVITYTYPE_MAINTENANCE.lower()):
        for index in df.index:
            itemDict = {}
            if (pd.notnull(df[COL_ASSETID][index]) 
            and pd.notnull(df[COL_MAINTENANCEDATE][index])
            and pd.notnull(df[COL_MAINTENANCECOST][index])):
                itemDict["itemReferenceId"] = df[COL_ASSETID][index]
                itemDict["transactionDate"] = str(df[COL_MAINTENANCEDATE][index])
                itemDict["totalAmount"] = df[COL_MAINTENANCECOST][index]
                itemDict["transactionType"] = ACTIVITYTYPE_MAINTENANCE
                itemDict["transactionSubType"] = str(df[COL_MAINTENANCETYPE][index] or '')
                jsonArray.append(itemDict)
            
    if(sys.argv[1].lower() == ACTIVITYTYPE_REPAIRS.lower()):
        for index in df.index:
            itemDict = {}
            itemDict["itemReferenceId"] = df[COL_ASSETID][index]
            
            if (pd.notnull(df[COL_REPLACEMENTCOST][index]) 
            or pd.notnull(df[COL_REPLACEMENTDATE][index])):
                if (pd.notnull(df[COL_ASSETID][index])
                and pd.notnull(df[COL_REPLACEMENTDATE][index]) 
                and pd.notnull(df[COL_REPLACEMENTCOST][index])):
                    itemDict["transactionDate"] = str(df[COL_REPLACEMENTDATE][index])
                    itemDict["totalAmount"] = df[COL_REPLACEMENTCOST][index]
                    itemDict["transactionType"] = ACTIVITYTYPE_REPLACEMENT
                    jsonArray.append(itemDict)
            else:
                if (pd.notnull(df[COL_ASSETID][index])
                and pd.notnull(df[COL_REPAIRDATE][index]) 
                and pd.notnull(df[COL_REPAIRCOST][index])):
                    itemDict["transactionDate"] = str(df[COL_REPAIRDATE][index])
                    itemDict["totalAmount"] = df[COL_REPAIRCOST][index]
                    itemDict["transactionType"] = ACTIVITYTYPE_REPAIRS
                    jsonArray.append(itemDict)
        
    
    
    #Uncomment below code if json data is to be written to file
    #jsonString = json.dumps(jsonArray)
    #f = open(JSON_FILE, "w")    
    #f.write(str(jsonString))
    #f.close()

    responseItems = requests.post(url = TRANSACTIONALSURL, json=jsonArray, headers = HEADERS)
    #response = responseItems.json()
    print (responseItems)

except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))
