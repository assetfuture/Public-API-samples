import os
import pip._vendor.requests

KEY = '<Subscription-key>'
AREAURL = "https://api.assetfuture.com/inventory/Areas"
ITEMURL = "https://api.assetfuture.com/inventory/Items"
HEADERS = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': KEY}
RECORDCOUNT = 10000
STARTINDEX = 0
CSVPATH = ".\\<FileName>.csv"
itemCount = RECORDCOUNT
areaCount = RECORDCOUNT
dictAreas = {}

try:
    #Delete if file already exists
    if os.path.exists(CSVPATH):
        os.remove(CSVPATH)
    
    #Get All records from Areas API
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
    with open(CSVPATH, 'a') as data_out :
        data_out.write("Space code,Region,Location,Block,Level,Area,Space Type,")
        data_out.write("Item Name,Quantity,Unit of Measure,Survey condition,survey date,")
        data_out.write("Item type1,Item type2,Item type3,item type4,RFID / Tag,Supplier,Brand,ModelNumber,Serial Number"+"\r")
        
        while itemCount >= RECORDCOUNT:
            PARAMS = {'count': RECORDCOUNT,'startIndex': STARTINDEX}
            print (PARAMS)
            responseItems = requests.get(url = ITEMURL, params = PARAMS, headers = HEADERS)
            items = responseItems.json()
            STARTINDEX = STARTINDEX + RECORDCOUNT
            itemCount = items["count"]
            print(items)
            
            #Transformation for CSV generation
            #Data records
            for item in items["data"]:                
                #format area path for extracting area related fields
                if item["area"] is not None and item["area"].strip("\\").count("\\") < 5 :
                    newAreaPath = item["area"].strip("\\").rjust(5-item["area"].strip("\\").count("\\")+len( item["area"].strip("\\")),"\\")
                elif item["area"] is not None and item["area"].strip("\\").count("\\") >= 5 :
                    newAreaPath = item["area"].strip("\\")
                else : newAreaPath = "".rjust(5,"\\")
                areaHierarchy = newAreaPath.split("\\")
                if dictAreas.get(item["area"],'') != '':
                    spaceCode = str(dictAreas.get(item["area"])["shortName"] or '')
                    spaceType = str(dictAreas.get(item["area"])["type"] or '')
                else:
                    spaceCode = ''
                    spaceType = ''
                data_out.write(spaceCode + ",")
                data_out.write(areaHierarchy[0].strip("\\") + ",")
                data_out.write(areaHierarchy[1].strip("\\") + ",")
                data_out.write(areaHierarchy[2].strip("\\") + ",")
                data_out.write(areaHierarchy[3].strip("\\") + ",")
                data_out.write(areaHierarchy[4].strip("\\") + ",")
                data_out.write(spaceType + ",")

                data_out.write(str(item["name"] or '').replace('# ', '').replace('$ ', '') + ",")
                data_out.write(str(item["quantity"] or '') + ",")
                data_out.write(str(item["unitOfMeasure"] or '') + ",")
                data_out.write(str(item["surveyCondition"] or '') + ",")
                data_out.write(str(item["surveyConditionDate"] or '') + ",")
                
                #format item type path for extracting item type fields
                if item["typePath"] is not None and item["typePath"].strip("\\").count("\\") < 5 :
                    newItemTypePath = item["typePath"].strip("\\").ljust(5-item["typePath"].strip("\\").count("\\")+len( item["typePath"].strip("\\")),"\\")
                elif item["typePath"] is not None and item["typePath"].strip("\\").count("\\") >= 5 :
                    newItemTypePath = item["typePath"].strip("\\")
                else : newItemTypePath = "".ljust(5,"\\")
                itemHierarchy = newItemTypePath.split("\\")
                data_out.write(itemHierarchy[0].strip("\\") + ",")
                data_out.write(itemHierarchy[1].strip("\\") + ",")
                data_out.write(itemHierarchy[2].strip("\\") + ",")
                data_out.write(itemHierarchy[3].strip("\\") + ",")
                data_out.write(str(item["trackingIdentifier"] or '') + ",")
                data_out.write(str(item["supplierName"] or '') + ",")
                data_out.write(str(item["proprietaryName"] or '') + ",")
                data_out.write(str(item["modelNo"] or '') + ",")
                data_out.write(str(item["serialNo"] or ''))
                data_out.write("\r")
    
except Exception as e:
    print("Error {0}: {1}".format(e.errno, e.strerror))