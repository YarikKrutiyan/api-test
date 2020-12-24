import requests
# from api.main_api import Authorization

from src.config import USER_MY


def routes(hosts, token):

    url = hosts + "/api/v1.1/routes/sync"

    payload = "{\n\t\"company_id\": 587\n}"
    headers = {
      'Authorization': f'Bearer {token}',
      'Content-Type': 'application/json',
      'Cookie': 'csrftoken=cK6QDPkZ2YdNNiSSHu0w6o7I11rWJmET05oR46kfCYUZIjy8qohk4Iaxfwt5yD2Y; sessionid=oei8of3a7hyhph73u6kjbt7rkcorecai'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.json())
    return response.json()


host = "https://test.agro-online.com"

t = Authorization.authorization(host, USER_MY).json()['token']
routes(host, t)