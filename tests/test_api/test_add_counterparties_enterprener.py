from api.auth.api_authorization import authorization
from src.config import USER_MY
from src.endpoint import Counterparties
from src.base_api import post
import pytest
from src.lib import create_random_string, request_to_db
from src.sql_request import SELECT_FULL_NAME_CONTERPATY


@pytest.fixture(scope="function", autouse=False)
def dict_for_test(hosts):
    test_data = dict(company_id=hosts['company_id'], fullname=create_random_string(11),
                     registration_type='entrepreneur', business_relations=['land'],
                     identify_number=create_random_string(10),
                     passport="PP666666", phone="+380667776677", address=create_random_string(10),
                     email="Petrenko@gmail.com", card_numbers=["5168745015631945"],
                     ibans=["CY17002001280000001200527600"],
                     date_of_birth="1966-06-06", date_of_death='2020-01-06', note=create_random_string(30))
    return test_data


@pytest.fixture(scope="function", autouse=False)
def dict_for_mandatory(hosts):
    test_data = dict(company_id=hosts['company_id'], fullname=create_random_string(30),
                     registration_type='company', business_relations=['land'])
    return test_data


class TestAddCounterpatiesEntrepreneur:

    @pytest.mark.parametrize('registration_type', ['entrepreneur', 'person'])
    def test_add_all_fields(self, hosts, dict_for_test, registration_type):
        dict_for_test['registration_type'] = registration_type
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert dict_for_test['fullname'] == add_counterpaties.json()[
            'fullname'], "Send key fullname not match the answer"
        assert dict_for_test['registration_type'] == add_counterpaties.json()[
            'registration_type'], "Send key registration_type not match the answer"
        assert dict_for_test['business_relations'] == add_counterpaties.json()[
            'business_relations'], "Send key business_relations not match the answer"
        assert dict_for_test['identify_number'] == add_counterpaties.json()[
            'identify_number'], "Send key identify_number not match the answer"
        assert dict_for_test['passport'] == add_counterpaties.json()['person'][
            'passport'], "Send key passport not match the answer"
        assert dict_for_test['phone'] == add_counterpaties.json()['phone'], "Send key phone not match the answer"
        assert dict_for_test['address'] == add_counterpaties.json()['address'], "Send key address not match the answer"
        assert dict_for_test['email'] == add_counterpaties.json()['person'][
            'email'], "Send key email not match the answer"
        assert dict_for_test['card_numbers'] == add_counterpaties.json()['payment_info'][
            'card_numbers'], "Send key card_numbers not match the answer"
        assert dict_for_test['ibans'] == add_counterpaties.json()['payment_info'][
            'ibans'], "Send key ibans not match the answer"
        assert dict_for_test['date_of_birth'] == add_counterpaties.json()['person'][
            'date_of_birth'], "Send key date_of_birth not match the answer"
        assert dict_for_test['date_of_death'] == add_counterpaties.json()['person'][
            'date_of_death'], "Send key date_of_death not match the answer"
        assert dict_for_test['note'] == add_counterpaties.json()['note'], "Send key note not match the answer"


    @pytest.mark.parametrize('registration_type', ['entrepreneur', 'person'])
    def test_add_mandatory_fields(self, hosts, dict_for_mandatory, registration_type):
        dict_for_mandatory['registration_type'] = registration_type
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_mandatory)
        assert dict_for_mandatory['fullname'] == add_counterpaties.json()['fullname']
        assert dict_for_mandatory['registration_type'] == add_counterpaties.json()['registration_type']
        assert dict_for_mandatory['business_relations'] == add_counterpaties.json()['business_relations']

    @pytest.mark.parametrize('business_relations', [['land'], ['supplier'], ['partner']])
    def test_add_mandatory_fields_all_business_relations(self, hosts, dict_for_mandatory, business_relations):
        dict_for_mandatory['business_relations'] = business_relations
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_mandatory)
        assert add_counterpaties.status_code == 200

    def test_add_counterparties_without_company_id(self, hosts, dict_for_test):
        dict_for_test['company_id'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without company id'
        assert add_counterpaties.json()['errors']['company_id'][0] == 2000, 'company id is Required field'

    def test_add_counterparties_with_int_company_id(self, hosts, dict_for_test):
        dict_for_test['company_id'] = "dsds"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with int company id'
        assert add_counterpaties.json()['errors']['company_id'][0] == 2002, 'company id is not integer'

    def test_add_counterparties_no_acces_company_id(self, hosts, dict_for_test):
        token = authorization(hosts['endpoint'], USER_MY).json()['token']
        dict_for_test['company_id'] = 254
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, token,
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create no acces to company id'
        assert add_counterpaties.json()['errors']['company_id'][0] == 2009, 'no acces to company'

    def test_add_counterparties_without_fullname(self, hosts, dict_for_test):
        dict_for_test['fullname'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create wthout fullname'
        assert add_counterpaties.json()['errors']['fullname'][0] == 2000, 'fullname is Required field'

    def test_add_counterparties_with_fullname_301symbol(self, hosts, dict_for_test):
        dict_for_test['fullname'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create wth fullname >300symbol'
        assert add_counterpaties.json()['errors']['fullname'][0] == 2001, 'fullname is Lenght exeeded'

    def test_add_counterparties_with_fullname_object_already_exists(self, hosts, dict_for_test):
        dict_for_test['fullname'] = \
            request_to_db(hosts['db_name'], SELECT_FULL_NAME_CONTERPATY.replace('0000', str(hosts['company_id'])))[0]
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with already exists fullname'
        assert add_counterpaties.json()['errors']['fullname'][0] == 2015, 'fullname already exists'

    def test_add_counterparties_without_registration_type(self, hosts, dict_for_test):
        dict_for_test['registration_type'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create wthout registration_type'
        assert add_counterpaties.json()['errors']['registration_type'][0] == 2000, 'registration_type is Required field'

    def test_add_counterparties_with_registration_type_random_str(self, hosts, dict_for_test):
        dict_for_test['registration_type'] = 'sdsf'
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with registration_type random string'
        assert add_counterpaties.json()['errors']['registration_type'][
                   0] == 2014, 'registration_type is Value should be from Enum'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-848
    def test_add_counterparties_without_business_relations(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without  business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][
                   0] == 2000, 'business_relations is 	Required field'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-844
    def test_add_counterparties_with_business_relations_massiv(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = []
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create without  business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][
                   0] == 2000, 'business_relations is 	Required field'

    def test_add_counterparties_with_business_relations_str(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = 'dsd'
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with no massive in business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][0] == 2017, 'business_relations is Array field'

    def test_add_counterparties_with_business_relations_invalid_type(self, hosts, dict_for_test):
        dict_for_test['business_relations'] = ['dsd']
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with invalid_type in business_relations'
        assert add_counterpaties.json()['errors']['business_relations'][0] == 2018, 'business_relations is invalid_type'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-845
    def test_add_counterparties_without_identify_number(self, hosts, dict_for_test):
        dict_for_test['identify_number'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without identify_number'

    def test_add_counterparties_with_identify_number_lenght_exeeded(self, hosts, dict_for_test):
        dict_for_test['identify_number'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with identify_number in Lenght exeeded'
        assert add_counterpaties.json()['errors']['identify_number'][0] == 2001, 'identify_number is Lenght exeeded'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-857
    def test_add_counterparties_with_passport_lenght_exeeded(self, hosts, dict_for_test):
        dict_for_test['passport'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with passport in Lenght exeeded'
        assert add_counterpaties.json()['errors']['passport'][0] == 2001, 'passport is Lenght exeeded'

    def test_add_counterparties_without_passport(self, hosts, dict_for_test):
        dict_for_test['passport'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without passport'

    def test_add_counterparties_with_phone_lenght_exeeded(self, hosts, dict_for_test):
        dict_for_test['phone'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with phone in Lenght exeeded'
        assert add_counterpaties.json()['errors']['phone'][0] == 2001, 'phone is Lenght exeeded'

    def test_add_counterparties_with_phone_type_field(self, hosts, dict_for_test):
        dict_for_test['phone'] = "lkfjfsd"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with phone in string'
        assert add_counterpaties.json()['errors']['phone'][0] == 2024, 'Phone type field'

    def test_add_counterparties_without_phone(self, hosts, dict_for_test):
        dict_for_test['phone'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without phone'

    def test_add_counterparties_without_address(self, hosts, dict_for_test):
        dict_for_test['address'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without address'

    def test_add_counterparties_with_address_lenght_exeeded(self, hosts, dict_for_test):
        dict_for_test['address'] = create_random_string(301)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with address in Lenght exeeded'
        assert add_counterpaties.json()['errors']['address'][0] == 2001, 'address is Lenght exeeded'

    def test_add_counterparties_without_email(self, hosts, dict_for_test):
        dict_for_test['email'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without email'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-858
    def test_add_counterparties_with_email_lenght_exeeded(self, hosts, dict_for_test):
        dict_for_test['email'] = "agro@gmail.com" + create_random_string(295)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with email in Lenght exeeded'
        assert add_counterpaties.json()['errors']['email'][0] == 2001, 'email is Lenght exeeded'

    def test_add_counterparties_with_email_type_field(self, hosts, dict_for_test):
        dict_for_test['email'] = create_random_string(15)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with email type field'
        assert add_counterpaties.json()['errors']['email'][0] == 2003, 'Email type field'

    def test_add_counterparties_without_card_numbers(self, hosts, dict_for_test):
        dict_for_test['card_numbers'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without card_numbers'

    def test_add_counterparties_with_card_numbers_array(self, hosts, dict_for_test):
        dict_for_test['card_numbers'] = "dssd"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with card_numbers Array field'
        assert add_counterpaties.json()['errors']['card_numbers'][0] == 2017, 'card_numbers Array field'

    def test_add_counterparties_with_card_numbers_invalid_type(self, hosts, dict_for_test):
        dict_for_test['card_numbers'] = [123]
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with card_numbers Array field'
        assert add_counterpaties.json()['errors']['card_numbers'][0] == 2018, 'card_numbers Array field'

    def test_add_counterparties_without_ibans(self, hosts, dict_for_test):
        dict_for_test['ibans'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without ibans'

    def test_add_counterparties_with_ibans_array(self, hosts, dict_for_test):
        dict_for_test['ibans'] = "dssd"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with ibans Array field'
        assert add_counterpaties.json()['errors']['ibans'][0] == 2017, 'ibans Array field'

    def test_add_counterparties_with_ibans_invalid_type(self, hosts, dict_for_test):
        dict_for_test['ibans'] = [123]
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with ibans invalid_type'
        assert add_counterpaties.json()['errors']['ibans'][0] == 2018, 'ibans invalid_type'

    def test_add_counterparties_without_date_of_birth(self, hosts, dict_for_test):
        dict_for_test['date_of_birth'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without date_of_birth'

    def test_add_counterparties_with_date_of_birth(self, hosts, dict_for_test):
        dict_for_test['date_of_birth'] = "dsd"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with date_of_birth invalid_type'
        assert add_counterpaties.json()['errors']['date_of_birth'][0] == 2011, 'date_of_birth invalid_type'

    def test_add_counterparties_without_date_of_death(self, hosts, dict_for_test):
        dict_for_test['date_of_death '] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without date_of_death'

    def test_add_counterparties_with_date_of_death(self, hosts, dict_for_test):
        dict_for_test['date_of_death'] = "dsd"
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with date_of_death invalid_type'
        assert add_counterpaties.json()['errors']['date_of_death'][0] == 2011, 'date_of_death invalid_type'

    @pytest.mark.xfail
    # https://agro-online.atlassian.net/browse/BT-846
    def test_add_counterparties_without_note(self, hosts, dict_for_test):
        dict_for_test['note'] = None
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 200, 'create without note'

    def test_add_counterparties_with_note(self, hosts, dict_for_test):
        dict_for_test['note'] = create_random_string(302)
        add_counterpaties = post(hosts['endpoint'], Counterparties.add_counterpaties_endpoint, hosts['tokens']['token'],
                                 dict_for_test)
        assert add_counterpaties.status_code == 400, 'cant create with note Lenght exeeded'
        assert add_counterpaties.json()['errors']['note'][0] == 2001, 'note Lenght exeeded'
