# Reading an excel file using Python
from numpy import nan
import pandas as pd
import requests

#Replace with your api subscription key.
#Generated after signing-up to the developer portal.
#To retrieve subscription key, sign-in to developer portal and access "Try it" section for any API
KEY = '<SUBSCRIPTION-KEY>'

#API URL to access
ITEMURL = "https://api.assetfuture.com/inventory/Items"

#Mandatory headers to be passed along with the request
HEADERS = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': KEY,}

#CSV File
#Row number where header is located
HEADER_ROW_NUM = 0
INDEX = 1
CSV_FILE = ".\\<FileName>.xlsx"
DATA_SHEET = "<Excel-sheet-name>"
areaProcessedDict = {}
jsonArray = []
try:

    #Read data from excel
    # Step1: Read projectName: - Needed for area path          
    Project = pd.read_excel(CSV_FILE, DATA_SHEET, index_col=None, usecols = "B", header = 1, nrows=0)
    Project = Project.columns.values[0]
    print(Project)

    #step2: Read Items data and prepare the json formatted data
    data = pd.read_excel (CSV_FILE, sheet_name=DATA_SHEET,header = HEADER_ROW_NUM)
    df = pd.DataFrame(data, columns= ['New Asset ID*','Site*','Quadrent','Building','Level','Room','System','Sub System','Component',
    'Asset Description*','Manufacturer*','Model Number*','Asset Category*','Qty','Capacity*','Capacity UOM*','Condition', 'Condition Date',
    'Install date *','Importance','Duty Factor','Item cost Factor','Area Cost Factor','Replacement Condition*','Maintenance Strategy*'])
    
    for index in df.index:
        itemDict = {}
        extensionDictionary = {}
        extensionJsonArray = []
        itemDict["name"] = df['Component'][index].strip()
        itemDict["shortName"] = df['Component'][index].strip()
        itemDict["referenceId"] = df['New Asset ID*'][index].strip()
        itemDict["typePath"] = df["System"][index].strip() + "\\" + df["Sub System"][index].strip()
        itemDict["area"] = "\\" + Project + "\\" + df["Quadrent"][index].strip() + "\\" + df["Building"][index].strip() + "\\" + df["Level"][index].strip() + "\\" + df["Room"][index].strip()
        itemDict["quantity"] = int(df['Qty'][index] or None)
        itemDict["surveyCondition"] = float(df['Condition'][index] or None)
        itemDict["notes"] = df['Asset Description*'][index].strip()
        itemDict["strategy"] = df['Maintenance Strategy*'][index]
        itemDict["dutyFactor"] = float(df['Duty Factor'][index])
        itemDict["manufacturer"] = df['Manufacturer*'][index]
        itemDict["modelNo"] = df['Model Number*'][index]
        if str(df['Install date *'][index]  or None) is not nan : 
           itemDict["installedDate"] = str(df['Install date *'][index])
        extensionDictionary["describe"] = 'Asset Category*'
        extensionDictionary["valueChar"] = str(df['Asset Category*'][index] or None)
        extensionJsonArray.append(extensionDictionary)
        extensionDictionary = {}
        extensionDictionary["describe"] = 'Capacity*'
        extensionDictionary["valueDouble"] = str(df['Capacity*'][index] or None)
        extensionJsonArray.append(extensionDictionary)
        extensionDictionary = {}
        extensionDictionary["describe"] = 'Asset Category*'
        extensionDictionary["valueChar"] = str(df['Asset Category*'][index] or None)        
        extensionJsonArray.append(extensionDictionary)
        itemDict["extensions"] = extensionJsonArray
        extensionDictionary = {}
        jsonArray.append(itemDict)

    responseItems = requests.post(url = ITEMURL, json=jsonArray, headers = HEADERS)
    response = responseItems.json()
    print (response)

except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))
