from src.lib import request_to_db
from src.sql_request import SELECT_TARGET_FIELD_ID
from src.base_api import get_with_url_params
from src.endpoint import Analyzes


class TestAnalyzesByField:

    def test_analyzes_by_field_positive(self, hosts):
        analyzes = get_with_url_params(hosts['endpoint'], Analyzes.analyze, hosts['tokens']['token'],
                                       dict(company_id=hosts['company_id']), request_to_db(hosts['db_name'],
                                       SELECT_TARGET_FIELD_ID.replace('0000', str(hosts['company_id'])))[0])

        assert analyzes.status_code == 200, 'Status code note valid'

