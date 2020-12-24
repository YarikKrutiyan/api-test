from src.base_api import get
from src.endpoint import CultureList


class TestCatalogCultureList:

    def test_get_catalog_culture_list(self, hosts):
        """Проверка позитивного сценария"""
        culture_list = get(hosts['endpoint'], CultureList.culture_list_endpoint, hosts['tokens']['token'],
                           dict(company_id=hosts['company_id']))
        assert culture_list.status_code == 200, 'Request failed, status code not 200'
        assert culture_list.json()['count'] == 40, 'Does not meet the number of cultures'
