from src.sql_request import SELECT_COUNT_LAND
from src.lib import request_to_db
from src.base_api import get
from src.endpoint import Lands


class TestGetLands:

    def test_get_lands_positive_with_filter_by_company_id(self, hosts):
        lands_list = get(hosts['endpoint'], Lands.get_lands, hosts['tokens']['token'],
                         dict(company_id=hosts['company_id']))
        assert lands_list.status_code == 200, 'Request failed, status code not 200'
        assert lands_list.json()['count'] == request_to_db(hosts['db_name'],
                                                           SELECT_COUNT_LAND.replace('0000', str(hosts['company_id'])))[0], \
            'The number of fields in the database and api is not the same'
