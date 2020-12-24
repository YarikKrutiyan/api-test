import requests
import json
from src.config import USER


def authorization(host, user):
    url = host + "/api/v1.1/auth/user/sign-in"
    payload = json.dumps(user)
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    return response



