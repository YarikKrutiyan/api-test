import requests
from flask import json
import urllib.parse


def field_reports(host, token, data):
    url = host + "/api/v1.1/field-reports"
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def send_file_for_report(host, token, company_id, report_id):
    data_json = urllib.parse.quote(json.dumps({'company_id': company_id, 'report_id': report_id}))
    url = host + f"/api/v1.1/field-reports/media?json=" + data_json

    payload = {}
    files = [
        ('files', open('../../img/2020-07-29_09-55.png', 'rb'))
    ]
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.json())
    return response


def send_file_for_report_alert(host, token, company_id, report_id, alert_id):
    data_json = urllib.parse.quote(json.dumps({'company_id': company_id, 'report_id': report_id, 'alert_id': alert_id}))
    url = host + f"/api/v1.1/field-reports/media?json=" + data_json

    payload = {}
    files = [
        ('files', open('../../img/2020-07-29_09-55.png', 'rb'))
    ]
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response
