import requests

response = requests.get(url = "https://api.assetfuture.com/inventory/Areas", 
                        params = {'count': 1,'alldata':False}, 
                        headers = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': '1474111d4b3a4982bb41f838b26f9b17'})

areas = response.json()

for area in areas["data"]:
    print("Name::" + area["name"])
    print("areaPath::" + area["areaPath"])

#print(areas)                        

response = requests.get(url = "https://api.assetfuture.com/inventory/Areas", 
                        params = {'count': 1,'alldata':False}, 
                        headers = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': '1474111d4b3a4982bb41f838b26f9b17'})

areas = response.json()

for area in areas["data"]:
    print("Name::" + area["name"])
    print("areaPath::" + area["areaPath"])