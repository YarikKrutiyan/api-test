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

headers = {'Content-Type': 'application/json'}
endpoint = "/api/v1.1/auth/user/sign-in"
set_environment = "https://test.agro-online.com"
company_id = 587
z = MainApi(headers)
print(z.auth_header())







