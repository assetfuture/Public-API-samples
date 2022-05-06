import csv
import json

#Replace with your api subscription key.
#Generated after signing-up to the developer portal.
#To retrieve subscription key, sign-in to developer portal and access "Try-it" section for any API
KEY = '<SUBSCRIPTION-KEY>'

#Api URL
AREAURL = "https://api.assetfuture.com/inventory/Areas"
#Headers to be sent
HEADERS = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': KEY,}
#Optional Parameters
PARAMS = {'count': 10000,'alldata':False}
#CSV File location
CSV_FILE = ".\\<FileName>.csv"

try:
    print("Send GET Request.")
    #Call the Area API
    response = requests.get(url = AREAURL, params = PARAMS, headers = HEADERS)
    print("Response Received.")
    #Parse the response as Json
    areas = response.json()
    csvData = ''
    csvHeader = "referenceId,type,region,status,name,shortName,importance,costFactor,latitude,longitude,notes,allowItems,contactPerson,email,mobile,phone,fax,street,city,suburb,postcode,state,createdWhen,createdBy,modifyWhen,modifyBy,numAreas,numItems,level,areaPath,"
    customFieldCount = 0
    #Transformation to CSV
    print('Transforming data.')
    for row in areas["data"]:
        i=0
        csvData = csvData + str(row["referenceId"] or '') + "," + str(row["type"] or '') + "," + str(row["region"] or '') + "," + str(row["status"] or '') + "," 
        csvData = csvData + str(row["name"] or '') + "," + str(row["shortName"] or '') + "," + str(row["importance"] or '') + "," + str(row["costFactor"] or '') + "," 
        csvData = csvData + str(row["latitude"] or '') + "," + str(row["longitude"] or '') + "," + str(row["notes"] or '') + "," + str(row["allowItems"] or '') + "," 
        csvData = csvData + str(row["contactPerson"] or '') + "," + str(row["email"] or '') + "," + str(row["mobile"] or '') + "," + str(row["phone"] or '') + "," 
        csvData = csvData + str(row["fax"] or '') + "," + str(row["street"] or '') + "," + str(row["city"] or '') + "," + str(row["suburb"] or '') + "," 
        csvData = csvData + str(row["postcode"] or '') + "," + str(row["state"] or '') + "," + str(row["createdWhen"] or '') + "," + str(row["createdBy"] or '') + "," 
        csvData = csvData + str(row["modifyWhen"] or '') + "," + str(row["modifyBy"] or '') + "," + str(row["numAreas"] or '') + "," + str(row["numItems"] or '') + "," 
        csvData = csvData + str(row["level"] or '') + "," + str(row["areaPath"] or '') + ","
        #transform extensions to columns        
        if row["extensions"]:
            extensions = json.dumps(row["extensions"])
            for exRow in row["extensions"]:
                i=i+1
                if exRow["describe"]:
                    csvData = csvData + exRow["describe"] + "," + str(exRow["valueChar"] or str(exRow["valueInt"] or str(exRow["valueDouble"] or str(exRow["valueBit"] or str(exRow["valueDate"] or '')))))

                if i > customFieldCount:
                    customFieldCount = i
        csvData = csvData + "\r"

    while customFieldCount > 0:
        csvHeader = csvHeader + "CustomField,Value"
        customFieldCount =  customFieldCount - 1
    
    csvHeader = csvHeader + "\r"

    with open(CSV_FILE, 'a') as data_out :
        data_out.write(csvHeader + csvData)        
    print('CSV generated at ' + CSV_FILE)
except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))
