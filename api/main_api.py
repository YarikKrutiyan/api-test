import requests
import json

from src.config import USER_MY


class MainApi(object):
    set_environment = "https://test.agro-online.com"
    endpoint = "/api/v1.1/auth/user/sign-in"
    data = USER_MY

    def __init__(self,headers):
        self.headers = headers

    def url(self):
        return (self.set_environment + self.endpoint)

    def payload(self):
        return json.dumps(self.data)

    def header(self):
        return self.headers

    def auth_api(self):
        response = requests.request("POST", url=self.url(), headers=self.header(), data=self.payload())
        return response

    def auth_header(self):
        header_auth = {"Authorization": f"Bearer {self.auth_api().json()['token']}"}
        self.headers.update(header_auth)
        return self.headers

def authorization(host, user):
    url = host + "/api/v1.1/auth/user/sign-in"
    payload = json.dumps(user)
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    return response







