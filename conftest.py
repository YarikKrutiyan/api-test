import pytest
from datetime import datetime

from requests import post

from api.auth.api_authorization import authorization
from src import config
from src.config import USER

from src.lib import request_to_db
from src.sql_request import *
from src.base_api import post
from src.endpoint import FieldReports


def pytest_addoption(parser):
    parser.addoption(
        '-E', '--env', action='store', default='dev', help='Choose environment: local, prod or rc'
    )
    parser.addoption(
        '-H', '--headless', action='store_true', default=False, help='Activates browser "Headless" mode'
    )
    parser.addoption(
        '-C', '--company', action='store', default=254, type=int,
        help='Set a id of company that you want to use in tests'
    )


def domain(request):
    host = config.LOCAL_HOST

    option_value = request.config.getoption('--env')

    if option_value == 'prod':
        host = config.PROD_HOST
    elif option_value == 'rc':
        host = config.RC_HOST
    elif option_value == 'dev':
        host = config.DEV_HOST
    elif option_value == 'test':
        host = config.TEST_HOST

    return host


@pytest.fixture(scope="session", autouse=False)
def hosts(request):
    try:
        host = domain(request)[0]
        bd_name = domain(request)[1]
        token = authorization(host, USER).json()
        company_id = request.config.getoption("--company")
        return dict(endpoint=host, tokens=token, db_name=bd_name, company_id=company_id)
    except:
        host = domain(request)
        Error = authorization(host, USER)
        print(Error)


@pytest.fixture(scope="function", autouse=False)
def report(hosts):
    report_with_alert = dict(company_id=hosts['company_id'], date=datetime.now().strftime("%Y-%m-%d"),
                             section_id=int(request_to_db(hosts['db_name'],
                                                          SECTION_ID.replace('0000', str(hosts['company_id'])))[0]),
                             route_point_id=int(request_to_db(
                                 hosts['db_name'], ROUT_POINT_ID.replace('0000', str(hosts['company_id'])))[0]),
                             alerts=[dict(priority="high", has_hazard=True, weed_id=2, pest_id=None, disease_id=None)])
    report_response = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                           report_with_alert)
    data = dict(company_id=report_with_alert['company_id'], report_id=report_response.json()['id'],
                alert_id=report_response.json()['alerts'][0]['id'])
    return dict(report_response=report_response, data=data)