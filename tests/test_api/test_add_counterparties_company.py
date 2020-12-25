from src.endpoint import Counterparties
from src.base_api import post
import pytest
from src.lib import create_random_string, request_to_db
from src.sql_request import SELECT_FULL_NAME_CONTERPATY
# qqqqqqqqqqssssddd


@pytest.fixture(scope="function", autouse=False)
def dict_for_test(hosts):
    test_data = dict(company_id=hosts['company_id'], fullname= create_random_string(30),
                     registration_type = 'company', business_relations = ['land'], identify_number = create_random_string(10),
                             phone = '+380667776677', address = 'Petrenko@gmail.com', email = 'qwe@sas.com', note = 'sdfsd dsf')
    return test_data



class TestAddCounterpaties:

    @pytest.mark.parametrize('registration_type', ['company', 'entrepreneur', 'person'])
    def test_add_mandatory_fields(self, hosts, dict_for_test, registration_type):
        dict_for_test['registration_type'] = registration_type
        add_counterpaties = post(hosts['endpoint'],Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'], dict_for_test)
        assert dict_for_test['fullname'] == add_counterpaties.json() ['fullname']
        assert dict_for_test['registration_type'] == add_counterpaties.json() ['registration_type']
        assert dict_for_test['business_relations'] == add_counterpaties.json() ['business_relations']

    def test_add_mandatory_business_relations_all_type(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = ['land','supplier','partner','other']
        add_counterpaties = post(hosts['endpoint'],Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'], dict_for_test)
        assert dict_for_test['business_relations'] == add_counterpaties.json() ['business_relations']

    def test_add_mandatory_all_keys(self, hosts, dict_for_test):
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'], dict_for_test)
        assert add_counterpaties.status_code == 200
        assert dict_for_test['identify_number'] == add_counterpaties.json() ['identify_number']
        assert dict_for_test['phone'] == add_counterpaties.json() ['phone']
        assert dict_for_test['address'] == add_counterpaties.json() ['address']
        assert dict_for_test['email'] == add_counterpaties.json() ['email']
        assert dict_for_test['note'] == add_counterpaties.json() ['note']

    def test_add_counterparties_without_company_id(self, hosts, dict_for_test):
        dict_for_test['company_id'] = ''
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without company id'
        assert add_counterpaties.json()['errors']['company_id'][0] == 2000, 'company id is required field'

    def test_add_counterparties_with_int_company_id(self, hosts, dict_for_test):
        dict_for_test['company_id'] = 'вфывфы'
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without company id'
        assert add_counterpaties.json()['errors']['company_id'][0] == 2002, 'company id is not	Integer field'

    def test_add_counterparties_with_int_company_no_access(self, hosts, dict_for_test):
        dict_for_test['company_id'] = 100500
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without company id'
        assert add_counterpaties.json()['errors']['company_id'][0] == 2009, 'Resource forbidden (no access)'

    def test_add_counterparties_without_fullname(self, hosts, dict_for_test):
        dict_for_test['fullname'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without fullname'
        assert add_counterpaties.json()['errors']['fullname'][0] == 2000, 'Required field fullname'

    def test_add_counterparties_with_fullname_130k(self, hosts, dict_for_test):
        dict_for_test['fullname'] = create_random_string(1300000)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without fullname'
        assert add_counterpaties.json()['errors']['fullname'][0] == 2001, 'Required field fullname'


    def test_add_counterparties_with_fullname_object_already_exists(self, hosts, dict_for_test):
        dict_for_test['fullname'] = request_to_db(hosts['db_name'],SELECT_FULL_NAME_CONTERPATY.replace('0000', str(hosts['company_id'])))[0]
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with already exists fullname'
        assert add_counterpaties.json()['errors']['fullname'][0] == 2015, 'fullname already exists'

    def test_add_counterparties_without_registration_type(self, hosts, dict_for_test):
        dict_for_test['registration_type'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without registration_type'
        assert add_counterpaties.json()['errors']['registration_type'][0] == 2000, 'registration_type is Required field'

    def test_add_counterparties_with_registration_type_enums(self, hosts, dict_for_test):
        dict_for_test['registration_type'] = 'sdsfsf'
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without registration_type'
        assert add_counterpaties.json()['errors']['registration_type'][0] == 2014, 'registration_type Value should be from Enum'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-839
    def test_add_counterparties_without_business_relations(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][0] == 2000, 'business_relations Required field'

    @pytest.mark.xfail
    # https: // agro - online.atlassian.net / browse / BT - 841
    def test_add_counterparties_with_business_relations_masive(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = []
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][0] == 2000, 'business_relations Required field'

    def test_add_counterparties_with_business_relations_array_field(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = "dss"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with no Array field business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][0] == 2017, 'business_relations Array field'

    def test_add_counterparties_with_business_relations_invalid_type(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = ["dss"]
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with Invaid type of item in array business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][0] == 2018, 'business_relations Invaid type of item in array'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-833
    def test_add_counterparties_without_identify_number(self, hosts, dict_for_test):
        dict_for_test['identify_number'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200

    def test_add_counterparties_with_identify_number_301sumbols(self, hosts, dict_for_test):
        dict_for_test['identify_number'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with identify_number Lenght exeeded'
        assert add_counterpaties.json()['errors']['identify_number'][
                   0] == 2001, 'identify_number Lenght exeeded'

    def test_add_counterparties_without_phone(self, hosts, dict_for_test):
        dict_for_test['phone'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200

    def test_add_counterparties_with_phone_301sumbols(self, hosts, dict_for_test):
        dict_for_test['phone'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with identify_number Lenght exeeded'
        assert add_counterpaties.json()['errors']['phone'][
                   0] == 2001, 'identify_number Lenght exeeded'

    def test_add_counterparties_with_phone_type_field(self, hosts, dict_for_test):
        dict_for_test['phone'] = "dssds"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with identify_number Lenght exeeded'
        assert add_counterpaties.json()['errors']['phone'][
                   0] == 2024, 'identify_number Lenght exeeded'

    def test_add_counterparties_without_address(self, hosts, dict_for_test):
        dict_for_test['address'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200

    def test_add_counterparties_with_address_301sumbols(self, hosts, dict_for_test):
        dict_for_test['address'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with address Lenght exeeded'
        assert add_counterpaties.json()['errors']['address'][
                   0] == 2001, 'address Lenght exeeded'

    def test_add_counterparties_without_email(self, hosts, dict_for_test):
        dict_for_test['email'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-840
    def test_add_counterparties_with_email_301sumbols(self, hosts, dict_for_test):
        dict_for_test['email'] = "agro@gmail.com" + create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with email Lenght exeeded'
        assert add_counterpaties.json()['errors']['email'][
                   0] == 2001, 'email Lenght exeeded'

    def test_add_counterparties_with_email_field(self, hosts, dict_for_test):
        dict_for_test['email'] = create_random_string(10)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with email Email field'
        assert add_counterpaties.json()['errors']['email'][
                   0] == 2003, 'email Email field'

    def test_add_counterparties_with_note(self, hosts, dict_for_test):
        dict_for_test['note'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with note'
        assert add_counterpaties.json()['errors']['note'][
                   0] == 2001, 'note Lenght exeeded'
