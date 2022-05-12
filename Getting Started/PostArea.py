import requests

jsonArray = []
areaDict = {}
areaDict["referenceId"] = 'refAreaId-00029'
areaDict["Name"] = "Test Area 01"
areaDict["ShortName"] = "TestArea01"
areaDict["areaPath"] =  "AssetFuture Demo\\Test Area 01"
areaDict["type"] = "RmType\\Accom"
areaDict["region"] = "New South Wales"
areaDict["allowItems"]=1
jsonArray.append(areaDict)

response = requests.post(url = "https://api.assetfuture.com/inventory/Areas", 
                        json = jsonArray, 
                        headers = {'Cache-Control': 'no-cache',
                                    'Ocp-Apim-Subscription-Key': 'subscription-key',
                                    'sessionId':'77e18e33-1cdc-436d-946d-7c38bcb3509d'})

result = response.json()
print (result)