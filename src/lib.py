import time
import random
import string
import psycopg2
from src.base_api import post


def create_email():
    email = str(time.time()) + "@gmail.com"
    return email


def create_random_string(string_length):
    letters = string.ascii_letters
    number = string.digits
    password = ''.join(random.choice(letters) for i in range(string_length))
    return password

def create_random_digist(string_length):
    number = string.digits
    digist = ''.join(random.choice(number) for i in range(string_length))
    return digist
create_random_digist(12)


def request_to_db(db_name, what):
    conn = psycopg2.connect(host='173.212.222.46', user='agroonline', password='k&ILxh4KJ.=0N2G*', dbname=db_name)

    cursor = conn.cursor()
    try:
        cursor.execute(f"{what}")
        row = cursor.fetchall()[0]
        return row

    except:
        return None

    cursor.close()
    conn.close()


def ids_of_counterparties(hosts, dict_for_test, url):
    dict_for_test['company_id'] = hosts['company_id']
    array = []
    while len(array) < 5:
        dict_for_test['fullname'] = create_random_string(30)
        add_counterpaties = post(hosts['endpoint'], url, hosts['tokens']['token'],
                                 dict_for_test).json()['id']
        array.append(add_counterpaties)

    return array


def dict_from_two_array(key, value):
    array_to_dict = {}
    for i in range(len(key)):
        array_to_dict[key[i]] = value[i]
    return array_to_dict


def change_value_into_array(r):
    for i in range(3,len(r)):
        r[i] = None
        print(r)

