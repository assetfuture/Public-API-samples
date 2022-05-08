import requests

response = requests.get(url = "https://api.assetfuture.com/inventory/Areas", 
                        params = {'count': 1,'alldata':False}, 
                        headers = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': 'SubscriptionKey'})

areas = response.json()

for area in areas["data"]:
    print("Name::" + area["name"])
    print("areaPath::" + area["areaPath"])