import requests

url = "https://api.mobilitytwin.brussels/stib/speed"

data = requests.get(url, headers={
    'Authorization': 'Bearer [MY_API_KEY]'
}).json()