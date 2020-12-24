import pytest
from src.lib import *
from src.sql_request import SECTION_ID, ROUT_POINT_ID
from src.base_api import post
from src.endpoint import FieldReports
from datetime import datetime


@pytest.fixture(scope="function", autouse=False)
def dict_for_test(hosts):
    test_data = dict(company_id=hosts['company_id'], date=datetime.now().strftime("%Y-%m-%d"),
                     section_id=int(request_to_db(hosts['db_name'],
                                                  SECTION_ID.replace('0000', str(hosts['company_id'])))[0]),
                     route_point_id=int(request_to_db(hosts['db_name'],
                                                      ROUT_POINT_ID.replace('0000', str(hosts['company_id'])))[0]))
    return test_data


class TestCreateReport:

    def test_create_report_for_planned_route(self, hosts, dict_for_test):
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 200, 'Report dont create'
        assert create_report.json()['id'] is not None, 'Report id is None'

    def test_create_report_for_unplanned_route(self, hosts, dict_for_test):
        del dict_for_test['route_point_id']
        dict_for_test["additional_point"] = dict(route_id=None, field_id=None, point={
            "type": "Point",
            "coordinates": [
                50.39166574117816,
                30.649214796868243
            ]
        })
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 200, 'Report dont create'
        assert create_report.json()['id'] is not None, 'Report id is None'

    def test_create_report_with_alert(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="high", has_hazard=True, weed_id=2, pest_id=None, disease_id=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 200, 'Report dont create'

    def test_create_report_without_company_id(self, hosts, dict_for_test):
        dict_for_test['company_id'] = ''
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create reporn without company id'
        assert create_report.json()['errors']['company_id'][0] == 2000, 'cant create reporn without company_id'

    def test_create_report_with_int_company_id(self, hosts, dict_for_test):
        dict_for_test['company_id'] = 'dsdssd'
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report without company id'
        assert create_report.json()['errors']['company_id'][0] == 2002, 'cant create report with int in company id'

    def test_create_report_without_section_id(self, hosts, dict_for_test):
        dict_for_test['section_id'] = ''
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report without section id'
        assert create_report.json()['errors']['section_id'][0] == 2000, 'cant create report with no section_id'

    def test_create_report_with_int_section_id(self, hosts, dict_for_test):
        dict_for_test['section_id'] = 'dsdfs'
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with int section_id'
        assert create_report.json()['errors']['section_id'][0] == 2002, 'cant create report with int section_id'

    def test_create_report_with_no_db_section_id(self, hosts, dict_for_test):
        dict_for_test['section_id'] = 'dsdfs'
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with int section_id'
        assert create_report.json()['errors']['section_id'][0] == 2002, 'cant create report with int section_id'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-824
    def test_create_report_with_wrong_date(self, hosts, dict_for_test):
        dict_for_test['date'] = "2020.05.04"
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with int section_id'
        assert create_report.json()['errors']['date'][0] == 2011, 'cant create report with int section_id'

    def test_create_report_with_int_route_point_id(self, hosts, dict_for_test):
        dict_for_test['route_point_id'] = "dsfds"
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with int route point id'
        assert create_report.json()["errors"]["route_point_id"][0] == 2002, 'tried crete with int route point id'

    def test_create_reports_with_no_db_route_point_id(self, hosts, dict_for_test):
        dict_for_test['route_point_id'] = 123
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'cant create report with existing route point id'
        assert create_report.json()['errors']['route_point_id'][
                   0] == 2010, 'cant create report with existing route point id'

    def test_create_report_with_resource_forbidden_company_id(self, hosts, dict_for_test):
        dict_for_test['company_id'] = 15555662121
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report without company id'
        assert create_report.json()['errors']['company_id'][
                   0] == 2009, 'cant create report with NO DB record company id'

    def test_create_report_with_int_phase_id(self, hosts, dict_for_test):
        dict_for_test['phase_id'] = "111"
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report without phase_id'
        assert create_report.json()['errors']['phase_id'][0] == 2002, 'cant create report with int in phase_id'

    def test_create_report_with_no_db_record_phase_id(self, hosts, dict_for_test):
        dict_for_test['phase_id'] = 55555111
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with no DB record in phase_id'
        assert create_report.json()['errors']['phase_id'][0] == 2010, 'cant create report with NO DB record phase_id'

    def test_create_report_with_moisture_availability(self, hosts, dict_for_test):
        dict_for_test['moisture_availability'] = 0, 1
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with moisture_availability'
        assert create_report.json()['errors']['moisture_availability'][
                   0] == 2014, 'cant create report with moisture_availability'

    def test_create_report_with_soil_seed_temperature(self, hosts, dict_for_test):
        dict_for_test['soil_seed_temperature'] = '122d'
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with soil_seed_temperature'
        assert create_report.json()['errors']['soil_seed_temperature'][
                   0] == 2002, 'cant create report with int soil_seed_temperature'

    def test_create_report_with_soil_soil_temperature(self, hosts, dict_for_test):
        dict_for_test['soil_temperature'] = '122d'
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with soil_temperature'
        assert create_report.json()['errors']['soil_temperature'][
                   0] == 2002, 'cant create report with int soil_temperature'

    def test_create_report_with_soil_comment(self, hosts, dict_for_test):
        dict_for_test['comment'] = create_random_string(130000)
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with comment '
        assert create_report.json()['errors']['comment'][0] == 2001, 'cant create report with lenght exeeded comment'

    def test_create_report_with_alerts(self, hosts, dict_for_test):
        dict_for_test['alerts'] = ""
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts'][0] == 2017, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_alert_priority(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="1221", has_hazard=True, weed_id=2, pest_id=None, disease_id=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['priority'][0] == 2014, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_alert_has_hazard(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="high", has_hazard=12121, weed_id=2, pest_id=None, disease_id=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['has_hazard'][0] == 2013, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_alert_weed_id_int(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="high", has_hazard=True, weed_id="12", pest_id=None, disease_id=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['weed_id'][0] == 2002, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_alert_no_db(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [
            dict(priority="high", has_hazard=True, weed_id=1233344, pest_id=None, disease_id=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['weed_id'][0] == 2010, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_alert_pest_id_int(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="high", has_hazard=True, weed_id=2, pest_id="123", disease_id=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['pest_id'][0] == 2002, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_alert_pest_id_no_db(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="high", has_hazard=True, weed_id=2, pest_id=44444123, disease_id=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['pest_id'][0] == 2010, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_allert_disease_id_int(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="high", has_hazard=True, weed_id=2, pest_id=None, disease_id="121")]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['disease_id'][0] == 2002, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_allert_disease_id_id_no_db(self, hosts, dict_for_test):
        dict_for_test['alerts'] = [dict(priority="high", has_hazard=True, weed_id=2, pest_id=None, disease_id=12112323)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['alerts']['disease_id'][0] == 2010, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_additional_point_route_id_int(self, hosts, dict_for_test):
        dict_for_test['additional_point'] = [dict(route_id="12d", point={"type": "Point",
                                                                         "coordinates": [
                                                                             36.870524883270264,
                                                                             46.84142180448305]})]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['additional_point']['route_id'][
                   0] == 2002, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_additional_point_route_id_no_db(self, hosts, dict_for_test):
        dict_for_test['additional_point'] = [dict(route_id=12312312312, point={"type": "Point",
                                                                               "coordinates": [
                                                                                   36.870524883270264,
                                                                                   46.84142180448305]})]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['additional_point']['route_id'][
                   0] == 2010, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_additional_point_point_required_field(self, hosts, dict_for_test):
        dict_for_test['additional_point'] = [dict(route_id=None, point=None)]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['additional_point']['point'][0] == 2000, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_additional_point_point_geojson_type(self, hosts, dict_for_test):
        dict_for_test['additional_point'] = [dict(route_id=None, point="123123")]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['additional_point']['point'][0] == 2016, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_additional_point_geometry_empty(self, hosts, dict_for_test):
        dict_for_test['additional_point'] = [dict(route_id=None, point={"type": "Point",
                                                                               "coordinates": [
                                                                               ]})]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['additional_point']['point'][0] == 2041, 'cant create report with alert'

    @pytest.mark.xfail
    def test_create_report_with_additional_point_point_type_field(self, hosts, dict_for_test):
        dict_for_test['additional_point'] = [dict(route_id=None, point={"type": "Point",
                                                                               "coordinates": [
                                                                                   36.8705248832701264,
                                                                                   46.841421804418305,
                                                                                   36.870524883280121,
                                                                                   46.841421804418313]})]
        create_report = post(hosts['endpoint'], FieldReports.field_report_endpoint, hosts['tokens']['token'],
                             dict_for_test)
        assert create_report.status_code == 400, 'create report with alert'
        assert create_report.json()['errors']['additional_point']['point'][0] == 2045, 'cant create report with alert'

