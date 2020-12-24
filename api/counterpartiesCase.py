import requests
import json

from api.main_api import MainApi
from src.endpoint import CounterpartyEndpoints, AuthorizationEndpoint


class Counterparties(MainApi):
    def get(self, set_environment, endpoint, headers, data, company_id):
        head = Counterparties(set_environment,endpoint,headers,data).auth_header()
        url = set_environment+"/api/v1.1/counterparties"
        print(head)
        d = json.dumps(dict(company_id=company_id))
        counterparties_list = requests.request("GET", url=url, headers=head, data=d)
        print(counterparties_list.json())



data = {'email': 'parik_84@ukr.net', 'password': '693384'}
headers = {'Content-Type': 'application/json'}
endpoint = "/api/v1.1/auth/user/sign-in"
set_environment = "https://test.agro-online.com"
company_id = 587
z = Counterparties(set_environment,endpoint, headers, data)
print(z.auth_header())
print(z.get(set_environment,endpoint, headers, data, company_id))
















        # counterparties_list = requests.request("GET", url=url, headers=head), data=d)
        # if counterparties_list.status_code == 200:
        #     return counterparties_list.json()
        # else:
        #     return counterparties_list.json()


