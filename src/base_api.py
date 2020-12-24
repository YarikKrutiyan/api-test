import json

import requests
import urllib.parse


def post(host, endpoint, token, data):
    url = host + endpoint

    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def get(host, endpoint, token, data):
    url = host + endpoint

    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response


def get_with_url_params(host, endpoint, token, data, url_data):
    url = host + endpoint + str(url_data)
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response


def post_with_url_params(host, endpoint, token, data, file):
    data_json = urllib.parse.quote(json.dumps(data))
    url = host + endpoint + data_json

    payload = {}
    files = [
        ('files', open(file, 'rb'))
    ]
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def patch_with_url_params(host, endpoint, token, id, data,):
    url = host + endpoint + '/' + id
    payload = json.dumps(data)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response
