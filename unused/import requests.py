import requests
import json



url = "https://644c02dabc002146b56d2f88.kakao.com/api/v2/user/{USER_ID}/talk/entities"

response = requests.get(url)


if response.status_code == 200:

    entity_json = response.json()
    print(entity_json)
    
else:
    print("Failed to retrieve entity JSON. Status code:", response.status_code)
    