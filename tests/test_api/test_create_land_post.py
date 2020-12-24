import pytest

from src.config import *
from api.main_api import Authorization
from src.lib import create_random_string, request_to_db
from src.sql_request import SELECT_LAND_ID, SELECT_EXIST_TITLE
from src.base_api import post
from src.endpoint import Lands


@pytest.fixture(scope="session", autouse=False)
def check_test_data_before_test(hosts):
    land_id = request_to_db(hosts['db_name'], SELECT_LAND_ID.replace('0000', str(hosts['company_id'])))
    if land_id is not None:
        post(hosts['endpoint'], Lands.delete_land, hosts['tokens']['token'], land_id)
    return land_id


class TestCreateLAnd:

    @pytest.mark.xfail
    def test_create_land_posit(self, hosts, check_test_data_before_test):
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], CREATE_LAND_POSIT)
        assert land.status_code == 200, 'Status code not valid'
        delete = post(hosts['endpoint'], Lands.delete_land, hosts['tokens']['token'], check_test_data_before_test)
        assert delete.status_code == 200, 'Пай не удален'

    def test_create_land_with_occupy_title(self, hosts):
        exist_title = request_to_db(hosts['db_name'], SELECT_EXIST_TITLE.replace('0000', str(hosts['company_id'])))[0]
        ex_title = CREATE_LAND_POSIT.copy()
        ex_title['title'] = exist_title
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], ex_title)
        assert land.status_code == 400, 'Create land with exist title'
        assert land.json()['errors']['title'][0] == 2015, 'Code of error is not valid'

    def test_create_land_without_company_id(self, hosts):
        without_company_id = CREATE_LAND_POSIT.copy()
        without_company_id['company_id'] = None
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], without_company_id)
        assert land.status_code == 400, 'Create land without company_id'
        assert land.json()['errors']['company_id'][0] == 2000, 'Code of error is not valid'

    def test_create_land_without_shape(self, hosts):
        shape = CREATE_LAND_POSIT.copy()
        shape["shape"] = None
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], shape)
        assert land.status_code == 400, 'Create land without shape'
        print(land.json()['errors']['shape'][0] == 2000), 'Code of error is not valid'

    def test_create_land_with_field_id_int(self, hosts):
        field_id_int = CREATE_LAND_POSIT.copy()
        field_id_int["field_id"] = "dsdfssd"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], field_id_int)
        assert land.status_code == 400, 'Create land with field_id integer'
        assert land.json()['errors']['field_id'][0] == 2002, 'Code of error field_id - Integer field'

    def test_create_land_with_field_id_no_db(self, hosts):
        land_with_field_no_db = CREATE_LAND_POSIT.copy()
        land_with_field_no_db["field_id"] = 2011110
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], land_with_field_no_db)
        assert land.status_code == 400, 'Create land with field_id NoDB'
        assert land.json()['errors']['field_id'][0] == 2010, 'Code of error field_id - Object not found (no DB record)'

    def test_create_land_with_land_type_owner_form_id_int(self, hosts):
        land_type_owner_form_id_int = CREATE_LAND_POSIT.copy()
        land_type_owner_form_id_int["land_type_owner_form_id"] = "dsfsdfs"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], land_type_owner_form_id_int)
        assert land.status_code == 400, 'Cant create land with land_type_owner_form_id  integer'
        assert land.json()['errors']['land_type_owner_form_id'][
                   0] == 2002, 'Code of error land_type_owner_form_id - Integer field'

    def test_create_land_with_land_type_owner_form_id_no_db(self, hosts):
        land_type_owner_form_no_db = CREATE_LAND_POSIT.copy()
        land_type_owner_form_no_db["land_type_owner_form_id"] = 201000
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], land_type_owner_form_no_db)
        assert land.status_code == 400, 'Create land with land_type_owner_form_id NoDB'
        assert land.json()['errors']['land_type_owner_form_id'][
                   0] == 2010, 'Code of error land_type_owner_form_id - Object not found (no DB record)'

    def test_create_land_with_land_type_assignment_id_int(self, hosts):
        land_type_assignment_int = CREATE_LAND_POSIT.copy()
        land_type_assignment_int["land_type_assignment_id"] = "sdfsdf"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], land_type_assignment_int)
        assert land.status_code == 400, 'Cant create land with land_type_assignment_id  integer'
        assert land.json()['errors']['land_type_assignment_id'][
                   0] == 2002, 'Code of error land_type_assignment_id - Integer field'

    def test_create_land_with_land_type_assignment_id_no_db(self, hosts):
        land_type_assignment_no_db = CREATE_LAND_POSIT.copy()
        land_type_assignment_no_db["land_type_assignment_id"] = 201000
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], land_type_assignment_no_db)
        assert land.status_code == 400, 'Create land with land_type_assignment_id NoDB'
        assert land.json()['errors']['land_type_assignment_id'][
                   0] == 2010, 'Code of error land_type_assignment_id - Object not found (no DB record)'

    @pytest.mark.xfail
    def test_create_land_with_document_area(self, hosts):
        document_area = CREATE_LAND_POSIT.copy()
        document_area["document_area"] = 55.555544
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], document_area)
        assert land.status_code == 400, 'Cant create land with document_area Float field'
        assert land.json()['errors']['document_area'][0] == 2019, 'Code of error document_area - Float field'

    # https://agro-online.atlassian.net/browse/BT-801
    def test_create_land_with_status(self, hosts):
        status = CREATE_LAND_POSIT.copy()
        status["status"] = 22.23424
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], status)
        assert land.status_code == 400, 'Cant create land with status Value should be from Enum'
        assert land.json()['errors']['status'][0] == 2014, 'Code of error status - Value should be from Enum'

    def test_create_land_with_cadaster_number(self, hosts):
        сad_number = CREATE_LAND_POSIT.copy()
        сad_number['cadaster_number'] = create_random_string(130000)
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], сad_number)
        assert land.status_code == 400, 'Cant create land with cadaster number'
        assert land.json()["errors"]["cadaster_number"][0] == 2001, \
            'Code of errors status - cadaster number length exceeded'

    def test_create_land_with_document_date(self, hosts):
        document_date = CREATE_LAND_POSIT.copy()
        document_date['document_date'] = "выв"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], document_date)
        assert land.status_code == 400, 'Cant create land with document_date'
        assert land.json()["errors"]["document_date"][
                   0] == 2011, 'Code of errors status - document_date Daterange field'

    def test_create_land_with_document_series(self, hosts):
        document_series = CREATE_LAND_POSIT.copy()
        document_series['document_series'] = create_random_string(130000)
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], document_series)
        assert land.status_code == 400, 'Cant create land with document_series'
        assert land.json()["errors"]["document_series"][
                   0] == 2001, 'Code of errors status - document series Lenght exeeded'

    def test_create_land_with_reg_number_in_drp(self, hosts):
        reg_number_in_drrp = CREATE_LAND_POSIT.copy()
        reg_number_in_drrp['reg_number_in_DRRP'] = create_random_string(130000)
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], reg_number_in_drrp)
        assert land.status_code == 400, 'Cant create land with document_series'
        assert land.json()["errors"]["reg_number_in_DRRP"][
                   0] == 2001, 'Code of errors status - reg_number_in_drp Lenght exeeded'

    """Bug for test https://agro-online.atlassian.net/browse/BT-798"""

    @pytest.mark.xfail
    def test_create_land_with_reg_date_in_drrp(self, hosts):
        reg_number_in_drrp = CREATE_LAND_POSIT.copy()
        reg_number_in_drrp['reg_date_in_DRRP'] = "123.11.12"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], reg_number_in_drrp)
        assert land.status_code == 400, 'Cant create land with document_series'
        assert land.json()["errors"]["reg_date_in_DRRP"][
                   0] == 2007, 'Code of errors status - reg_number_in_drrp Daterange field'

    def test_create_land_with_ngo_value(self, hosts):
        ngo_value = CREATE_LAND_POSIT.copy()
        ngo_value['ngo_value'] = "dsdffs"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], ngo_value)
        assert land.status_code == 400, 'Cant create land with document_series'
        assert land.json()["errors"]["ngo_value"][
                   0] == 2019, 'Code of errors status - reg_number_in_drrp Daterange field'

    def test_create_land_alert(self, hosts):
        alert = CREATE_LAND_POSIT.copy()
        alert['alert'] = "dsdffs"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], alert)
        assert land.status_code == 400, 'Cant create land with alert'
        assert land.json()["errors"]["alert"][0] == 2013, 'Code of errors status - alert Boolean field'

    def test_create_land_company_id_int(self, hosts):
        company_id_int = CREATE_LAND_POSIT.copy()
        company_id_int["company_id"] = "dssd"
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], company_id_int)
        assert land.status_code == 400, "Cant create land with alert"
        assert land.json()["errors"]["company_id"][0] == 2002, 'Code of errors status - company_id Integer field'

    def test_create_lend_company_id_no_access(self, hosts):
        token = Authorization.authorization(hosts['endpoint'], USER_MY).json()['token']
        company_id_no_access = CREATE_LAND_POSIT.copy()
        company_id_no_access["company_id"] = 88
        land = post(hosts['endpoint'], Lands.create_land, token, company_id_no_access)
        assert land.status_code == 400, 'Create land without shape'
        assert land.json()['errors']['company_id'][0] == 2009, 'Code of error no access'

    def test_create_land_title_required_field(self, hosts):
        title_required_field = CREATE_LAND_POSIT.copy()
        title_required_field["title"] = None
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], title_required_field)
        assert land.status_code == 400, "Cant create winthout title"
        assert land.json()['errors']['title'][0] == 2000, 'Code of errors staus - title is required field'

    def test_create_land_title_lenght_exeeded(self, hosts):
        title_lenght_exeeded = CREATE_LAND_POSIT.copy()
        title_lenght_exeeded['title'] = create_random_string(130000)
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], title_lenght_exeeded)
        assert land.status_code == 400, "Cant create land with title"
        assert land.json()['errors']['title'][0] == 2001, "Code of errors status = title is Langht exeeded"

    def test_create_land_shape_geojson_type(self, hosts):
        shape_geojson_type = CREATE_LAND_POSIT.copy()
        shape_geojson_type['shape'] = 1231
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], shape_geojson_type)
        assert land.status_code == 400, "Cant create land with shape"
        assert land.json()['errors']['shape'][0] == 2016, "Code of errors status = shape is Geojson type"

    def test_create_land_shape_multi_polygon_type_field(self, hosts):
        shape_geojson_type = CREATE_LAND_POSIT.copy()
        shape_geojson_type['shape'] = MultiPolygon_type_field
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], shape_geojson_type)
        assert land.status_code == 400, "Cant create land with shape"
        assert land.json()['errors']['shape'][1] == 2038, "Code of errors status = shape is MultiPolygon type field"

    def test_create_land_shape_multipolygon_type_field_max_fact_area_exided(self, hosts):
        shape_geojson_type = CREATE_LAND_POSIT.copy()
        shape_geojson_type['shape'] = Polygon1001ha
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], shape_geojson_type)
        assert land.status_code == 400, "Cant create land with shape"
        assert land.json()['errors']['shape'][0] == 2039, "Code of errors status = shape is Shape max fact area exided"

    def test_create_land_shape_multipolygon_type_field_geometry_is_empty(self, hosts):
        shape_geojson_type = CREATE_LAND_POSIT.copy()
        shape_geojson_type['shape'] = Shape_geometry_empty
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], shape_geojson_type)
        assert land.status_code == 400, "Cant create land with shape"
        assert land.json()['errors']['shape'][0] == 2041, "Code of errors status = shape is Geometry is empty"

    def test_create_land_shape_multipolygon_type_field_numb_of_geometries_exided(self, hosts):
        shape_geojson_type = CREATE_LAND_POSIT.copy()
        shape_geojson_type['shape'] = Polygons6
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], shape_geojson_type)
        assert land.status_code == 400, "Cant create land with shape"
        assert land.json()['errors']['shape'][0] == 2040, "Code of errors status = shape is Numb of geometries exided"

    def test_create_land_shape_multipolygon_type_field(self, hosts):
        shape_geojson_type = CREATE_LAND_POSIT.copy()
        shape_geojson_type['shape'] = Polygon003ha
        land = post(hosts['endpoint'], Lands.create_land, hosts['tokens']['token'], shape_geojson_type)
        assert land.status_code == 400, "Cant create land with shape"
        assert land.json()['errors']['shape'][0] == 2043, "Code of errors status = shape is Numb of geometries exided"
