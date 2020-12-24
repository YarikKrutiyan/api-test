from src.base_api import post_with_url_params
from src.config import TEST_FILE
from src.endpoint import AddFileToReport


class TestAddMediaReport:

    def test_add_img_to_the_report_positive(self, hosts, report):
        send_img = post_with_url_params(hosts['endpoint'], AddFileToReport.add_file_endpoint, hosts['tokens']['token'],
                                        report['data'], TEST_FILE.get('path'))
        assert send_img.status_code == 200, 'File dont add to report'
        assert send_img.json()['link'] is not None, 'File link is missing'

    def test_add_img_to_the_alert(self, hosts, report):
        send_img = post_with_url_params(hosts['endpoint'], AddFileToReport.add_file_endpoint, hosts['tokens']['token'],
                                        report['data'], TEST_FILE.get('path'))

        assert send_img.status_code == 200, 'File dont add to report'
        assert send_img.json()['link'] is not None, 'File link is missing'
        assert send_img.json()['alert_id'] == report['report_response'].json()['alerts'][0]['id'], \
            'Alert id is not the same'

