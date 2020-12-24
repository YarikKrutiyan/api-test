import pytest

from api.auth.api_authorization import authorization
from src.base_api import post
from src.config import USER_MY
from src.endpoint import Counterparties
from src.lib import create_random_string
from src.lib import request_to_db
from src.sql_request import SELECT_CONTRPARTY_ID
from src.lib import ids_of_counterparties

dict_for_test_company = dict(company_id=None, registration_type='company', business_relations=['land'],
                             identify_number=create_random_string(10),
                             phone='+380667776677', address='Petrenko@gmail.com', email='qwe@sas.com', note='sdfsd dsf')

dict_for_test_entrepreneur = dict(company_id=None, fullname=create_random_string(30),
                                  registration_type='company', business_relations=['land'],
                                  identify_number=create_random_string(10),
                                  passport="PP666666", phone="+380667776677", address=create_random_string(10),
                                  email="Petrenko@gmail.com", card_numbers=["5168745015631945"],
                                  ibans=["CY17002001280000001200527600"],
                                  date_of_birth="1966-06-06", date_of_death='2020-01-06', note=create_random_string(30))


@pytest.fixture(scope="function", autouse=False)
def ids_of_counterparties_company(hosts):
    id = ids_of_counterparties(hosts, dict_for_test_company, Counterparties.add_counterpaties_endpoint)
    return id


@pytest.fixture(scope="function", autouse=False)
def ids_of_counterparties_entepreneur(hosts):
    ids = ids_of_counterparties(hosts, dict_for_test_entrepreneur, Counterparties.add_counterpaties_endpoint)
    return ids


class TestDeleteCounterparties:
    def test_posyt_del_one_counterparties_company(self, hosts, ids_of_counterparties_company):

        r_data = dict(company_id=hosts['company_id'], counterparties_ids=[ids_of_counterparties_company[0]])

        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)

        assert del_counterparties_company.status_code == 200, "Status code is not valid, counterparty has not been delete"
        assert request_to_db(hosts['db_name'], SELECT_CONTRPARTY_ID.replace('0000', str(
            ids_of_counterparties_company[0]))) is not None, "counterparty has not been deleted in DB"

    def test_posyt_del_one_counterparties_entrepreneur(self, hosts, ids_of_counterparties_entepreneur):
        r_data2 = dict(company_id=hosts['company_id'], counterparties_ids=[ids_of_counterparties_entepreneur[0]])
        del_counterparties_entrepreneur = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                               hosts['tokens']['token'], r_data2)

        assert del_counterparties_entrepreneur.status_code == 200, "Status code is not valid, counterparty has not been delete"
        assert request_to_db(hosts['db_name'], SELECT_CONTRPARTY_ID.replace('0000', str(
            ids_of_counterparties_entepreneur[0]))) is not None, "counterparty has not been deleted in DB"

    def test_posyt_del_many_counterparties_company(self, hosts, ids_of_counterparties_company):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=ids_of_counterparties_company)

        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)

        assert del_counterparties_company.status_code == 200, "Status code is not valid, counterparty has not been delete"
        for id in ids_of_counterparties_company:
            assert request_to_db(hosts['db_name'], SELECT_CONTRPARTY_ID.replace('0000', str(id)))[
                       0] is not None, "counterparty has not been deleted in DB"

    def test_posyt_del_many_counterparties_entrepreneur(self, hosts, ids_of_counterparties_entepreneur):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=ids_of_counterparties_entepreneur)

        del_counterparties_entrepreneur = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                               hosts['tokens']['token'], r_data)

        assert del_counterparties_entrepreneur.status_code == 200, "Status code is not valid, counterparty has not been delete"
        for id in ids_of_counterparties_entepreneur:
            assert request_to_db(hosts['db_name'], SELECT_CONTRPARTY_ID.replace('0000', str(id)))[
                       0] is not None, "counterparty has not been deleted in DB"

    def test_negat_del_counterparties_company_without_token(self, hosts, ids_of_counterparties_company):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=[ids_of_counterparties_company[0]])
        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          None, r_data)

        assert del_counterparties_company.status_code == 401, "Delete without token"

    def test_negat_del_counterparties_company_without_company_id(self, hosts, ids_of_counterparties_company):
        r_data = dict(counterparties_ids=[ids_of_counterparties_company[0]])
        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)

        assert del_counterparties_company.status_code == 400, "Status code is not valid, counterparty has not been delete"
        assert del_counterparties_company.json()['errors']['company_id'][0] == 2000, "Not valid error code"

    def test_negat_del_counterparties_company_without_counterparties_ids(self, hosts, ids_of_counterparties_company):
        r_data = dict(company_id=hosts['company_id'])
        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)

        assert del_counterparties_company.status_code == 400, "Status code is not valid, counterparty has not been delete"
        assert del_counterparties_company.json()['errors']['counterparties_ids'][1] == 2017, "Not valid error code"

    def test_negat_del_counterparties_without_access_company(self, hosts, ids_of_counterparties_company):
        token = authorization(hosts['endpoint'], USER_MY).json()['token']
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=[ids_of_counterparties_company[0]])

        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          token, r_data)
        assert del_counterparties_company.status_code == 400, "Status code is not valid"
        assert del_counterparties_company.json()['errors']['company_id'][0] == 2009, "Error code is note valid"
        assert request_to_db(hosts['db_name'], SELECT_CONTRPARTY_ID.replace('0000', str(
            ids_of_counterparties_company[0]))[0]) is None, "counterparty was deleted from DB"

    def test_negat_del_counterparties_id_not_into_array(self, hosts, ids_of_counterparties_company):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=ids_of_counterparties_company[0])

        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)
        assert del_counterparties_company.status_code == 400, "Status code is not valid, counterparty has not been delete"
        assert del_counterparties_company.json()['errors']['counterparties_ids'][0] == 2017, "Error code is note valid"
        assert request_to_db(hosts['db_name'], SELECT_CONTRPARTY_ID.replace('0000', str(
            ids_of_counterparties_company[0]))) is not None, "counterparty has not been deleted in DB"

    def test_negat_del_counterparties_id_empty_array(self, hosts, ids_of_counterparties_company):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=[None])

        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)
        assert del_counterparties_company.status_code == 400, "Status code is not valid, counterparty has not been delete"
        assert del_counterparties_company.json()['errors']['counterparties_ids'][0] == 2018, "Error code is note valid"

    def test_negat_del_counterparties_id_is_note_exist(self, hosts, ids_of_counterparties_company):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=[11000])

        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)
        assert del_counterparties_company.status_code == 400, "Status code is not valid, counterparty has not been delete"
        assert del_counterparties_company.json()['errors']['counterparties_ids'][0] == 2010, "Error code is note valid"

    def test_negat_del_counterparties_id_is_previously_deleted(self, hosts, ids_of_counterparties_company):
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=[ids_of_counterparties_company[0]])
        first_delete = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)
        assert first_delete.status_code == 200, "The precondition was not met."
        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)
        assert del_counterparties_company.status_code == 400, "Status code is not valid, counterparty has not been delete"
        assert del_counterparties_company.json()['errors']['counterparties_ids'][0] == 2010, "Error code is note valid"

    def test_negat_del_many_counterparties_with_one_note_exist(self, hosts, ids_of_counterparties_company):
        ids_of_counterparties_company.append(99999)
        r_data = dict(company_id=hosts['company_id'], counterparties_ids=ids_of_counterparties_company)
        del_counterparties_company = post(hosts['endpoint'], Counterparties.del_counterpaties_endpoint,
                                          hosts['tokens']['token'], r_data)
        assert del_counterparties_company.status_code == 400, "Status code is not valid, counterparty has not been delete"
        assert del_counterparties_company.json()['errors']['counterparties_ids'][0] == 2010, "Error code is note valid"





