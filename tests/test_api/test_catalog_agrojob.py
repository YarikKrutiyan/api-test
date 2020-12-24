from src.base_api import get
from src.endpoint import AgroJob


class TestCatalogAgroJob:

    def test_get_catalog_a(self, hosts):
        """Проверка позитивного сценария"""
        agro_job_list = get(hosts['endpoint'], AgroJob.agro_job_endpoint, hosts['tokens']['token'],
                            dict(company_id=hosts['company_id']))
        assert agro_job_list.status_code == 200, 'Request failed, status code not 200'
        assert agro_job_list.json()['count'] == 61, 'Does not meet the number of agro job'
