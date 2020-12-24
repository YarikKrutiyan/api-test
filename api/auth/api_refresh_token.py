import requests
import json



def refresh_token(host, refresh_token):
    url = host + "/api/v1.1/auth/refresh"

    payload = json.dumps({"refresh_token": refresh_token})
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

