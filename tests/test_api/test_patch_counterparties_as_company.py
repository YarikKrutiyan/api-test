import pytest

from api.main_api import Authorization
from src.base_api import patch_with_url_params, post
from src.config import USER_MY
from src.endpoint import Counterparties
from src.lib import ids_of_counterparties, create_random_string, create_random_digist, dict_from_two_array, \
    request_to_db
from src.sql_request import SELECT_FULL_NAME_CONTERPATY

dict_for_test = dict(company_id=None, fullname='Agro company B', registration_type='company',
                     business_relations=['land'],
                     identify_number='6666', phone='+380667776677', address='agro@gmail.com', email='agro@gmail.com',
                     note='some not')

array_of_key = ['company_id', 'fullname', 'registration_type', 'business_relations', 'identify_number', 'phone',
                'address', 'email', 'note']


@pytest.fixture(scope="function", autouse=False)
def ids_of_counterparties_company(hosts):
    ids = ids_of_counterparties(hosts, dict_for_test, Counterparties.add_counterpaties_endpoint)
    return ids


@pytest.fixture(scope="function", autouse=False)
def array_with_all_key(hosts):
    array_value = [hosts['company_id'], create_random_string(30), 'company', ['supplier'],
                   create_random_digist(6), '+38067' + create_random_digist(7), create_random_string(30),
                   create_random_string(5) + '@gmail.com', create_random_string(20)]
    update_dict = dict_from_two_array(array_of_key, array_value)
    return update_dict


class TestPatchCounterpartiesAsCompany:
    def test_positive_patch_counterparties_all_mandatory_filds(self, hosts, ids_of_counterparties_company,
                                                               array_with_all_key):
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)

        assert patch_counterparties.status_code == 200, 'The business partner has not been updated. Status code is not 200'
        assert patch_counterparties.json()['fullname'] == array_with_all_key['fullname']

    def test_positive_patch_try_to_update_identify_number_key_to_none(self, hosts, ids_of_counterparties_company,
                                                                      array_with_all_key):
        array_with_all_key['identify_number'] = None
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 200, 'The identify_number not updated. Status code is not 200'

    def test_positive_patch_try_to_update_phone_key_to_none(self, hosts, ids_of_counterparties_company,
                                                            array_with_all_key):
        array_with_all_key['phone'] = None
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 200, 'The phone not updated. Status code is not 200'

    def test_positive_patch_try_to_update_address_to_none(self, hosts, ids_of_counterparties_company,
                                                          array_with_all_key):
        array_with_all_key['address'] = None
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 200, 'The address not updated. Status code is not 200'

    def test_positive_patch_try_to_update_email_to_none(self, hosts, ids_of_counterparties_company, array_with_all_key):
        array_with_all_key['email'] = None
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 200, 'The email not updated. Status code is not 200'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-867
    def test_positive_patch_try_to_update_note_to_none(self, hosts, ids_of_counterparties_company, array_with_all_key):
        array_with_all_key['note'] = None
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 200, 'The note not updated. Status code is not 200'

    def test_negative_patch_try_to_update_registration_type(self, hosts, ids_of_counterparties_company,
                                                            array_with_all_key):
        array_with_all_key['registration_type'] = 'entrepreneur'
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)

        assert patch_counterparties.status_code == 400, 'The business_relations updated. Status code is 200'
        assert patch_counterparties.json()['errors']['registration_type'][0] == 2017, " Status code not valid"

    def test_negative_patch_without_access_to_company(self, hosts, ids_of_counterparties_company, array_with_all_key):
        token = Authorization.authorization(hosts['endpoint'], USER_MY).json()['token']
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     token, str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 400, "Can update without access to the company"
        assert patch_counterparties.json()['errors']['company_id'][0] == 2009, " Status code is note valid"

    def test_negative_patch_counterparties_id_is_note_exist(self, hosts, ids_of_counterparties_company,
                                                            array_with_all_key):
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], '00000',
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 400, "Status code is not valid. We cannot update a non-existent " \
                                                        "counterparty "
        assert patch_counterparties.json()['errors']['counterparty_id'][0] == 2010, "Error code is not valid"

    def test_negative_patch_counterparties_id_deleted(self, hosts, ids_of_counterparties_company, array_with_all_key):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=[ids_of_counterparties_company[0]])
        first_delete = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                            hosts['tokens']['token'], r_data)
        assert first_delete.status_code == 200, "The precondition was not met."
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 400, "Status code is not valid. We cannot update a non-existent " \
                                                        "counterparty "
        assert patch_counterparties.json()['errors']['counterparty_id'][0] == 2010, "Error code is not valid"

    def test_negative_patch_without_token(self, hosts, ids_of_counterparties_company, array_with_all_key):
        token = None
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     token, str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 401, "Can update without token "

    def test_negative_patch_occupied_name(self, hosts, ids_of_counterparties_company, array_with_all_key):
        array_with_all_key['fullname'] = \
        request_to_db(hosts['db_name'], SELECT_FULL_NAME_CONTERPATY.replace('0000', str(hosts['company_id'])))[0]
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 400, "It is possible to create with an existing name"
        assert patch_counterparties.json()['errors']['fullname'][0] == 2015, "Status code not valid"

    def test_negative_patch_business_relations_not_valid_value(self, hosts, ids_of_counterparties_company,
                                                               array_with_all_key):
        array_with_all_key['business_relations'] = ['not valid']
        patch_counterparties = patch_with_url_params(hosts['endpoint'], Counterparties.add_counterpaties_endpoint,
                                                     hosts['tokens']['token'], str(ids_of_counterparties_company[0]),
                                                     array_with_all_key)
        assert patch_counterparties.status_code == 400, "It is possible to create with an existing business_relations"
        assert patch_counterparties.json()['errors']['business_relations'][0] == 2018, "status code not valid"
