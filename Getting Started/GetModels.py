import requests
import uuid

SUBSCRIPTION_KEY = 'subscription-key'
MODELS_API_ENDPOINT = "https://api.assetfuture.com/inventory/Areas"
REQUEST_PARAMETERS = {'count': 1,'alldata':False}
REQUEST_HEADER = {'Cache-Control': 'no-cache','Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}

response = requests.get(url = MODELS_API_ENDPOINT, 
                        params = REQUEST_PARAMETERS, 
                        headers = REQUEST_HEADER)

areas = response.json()

for area in areas["data"]:
    print("Name::" + area["name"])
    print("areaPath::" + area["areaPath"])

