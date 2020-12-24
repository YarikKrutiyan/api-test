import os

# PROJECT_PATH = os.path.dirname(os.path.realpath('config.py'))

PROD_HOST = 'https://app.agro-online.com', 'app'
LOCAL_HOST = 'http://example.com:8000'
RC_HOST = 'https://rc.agro-online.com', 'rc'
DEV_HOST = 'https://dev.agro-online.com', 'dev'
TEST_HOST = 'https://test.agro-online.com', 'test'

USER = {
    'email': 'test-user@test.com',
    'password': ')pCeJDV6g8zyrXA'
}
USER_MY = {
    'email': 'parik_84@ukr.net',
    'password': '693384'
}

CREATE_LAND_POSIT = {"company_id": 254, "title": "TestQA", "shape": {"type": "MultiPolygon", "coordinates": [[[[
                                                                                                                   -111.27442359924316,
                                                                                                                   37.40560214747637],
                                                                                                               [
                                                                                                                   -111.27403736114502,
                                                                                                                   37.40490329864026],
                                                                                                               [
                                                                                                                   -111.27283573150635,
                                                                                                                   37.40553396738905],
                                                                                                               [
                                                                                                                   -111.27337217330933,
                                                                                                                   37.40662484134086],
                                                                                                               [
                                                                                                                   -111.27442359924316,
                                                                                                                   37.40560214747637]]]]},
                     "land_type_owner_form_id": None, "land_type_assignment_id": None, "document_area": 213.321,
                     "status": "ar", "cadaster_number": "3220483713:02:010:0008", "document_date": "2019-01-02",
                     "document_series": "32123daswer", "document_reg_number": "321", "reg_number_in_DRRP": "321jdsa",
                     "reg_date_in_DRRP": "2019-01-02", "ngo_value": 12.34, "alert": False}

FIELD_REPORT = {"company_id": 254,"date":"2019-01-02","route_point_id":1,"phase_id":1,"section_id": 12773,"moisture_availability": "medium","soil_seed_temperature": 20,"soil_temperature": 20,"comment": "ewqwqe231","alerts":[{"priority":"low","has_hazard":False,"weed_id": 2,"pest_id": None,"disease_id": None}],"additional_point": {"route_id": None,"field_id": None,"point": {
            "type": "Point",
            "coordinates": [
                36.870524883270264,
                46.84142180448305
            ]
        }}}
FIELD_REPORT_NONE = {"company_id": 254,"date":"2019-01-02","route_point_id":None,"phase_id":None,"section_id": None,"moisture_availability": None,"soil_seed_temperature": None,"soil_temperature": None,"comment": None,"alerts":None,"additional_point": None}

INVALID_USER = {
    'email': 'test-user1@testrrrrr.com',
    'password': '12345678wwww'
}

TEST_DATA = {
    'cadustr_number': '9999999999:99:999:9999',
}

TEST_FILE = {
    'path': os.path.abspath('src/img/2020-07-29_09-55.png')
}

MAILSLURP_TOKEN = 'f6d17f59f030854811079918e6a7de5590e2699ad63e3e6b46528aedd738e60d'

KADASTR_ARRAY = ['5120887200:01:002:1426']


class ErrorMessage(object):
    ERROR_LOGIN_EMAIL_MESSAGE = 'Пользователь не существует'
    ERROR_LOGIN_PASSWORD_MESSAGE = 'Введен неправильный пароль, повторите попытку'
    ERROR_CONFIRM_PASSWORD_MESSAGE = 'Введенные пароли не совпадают'
    ERROR_INVALID_PASSWORD_MESSAGE = 'Пароль должен содержать минимум 8 символов'
    ERROR_INVALID_EMAIL_MESSAGE = 'Введите правильный адрес электронной почты.'

"POlygons for tests"
Polygons_that_intersect = {        "type": "MultiPolygon","coordinates": [ [          [            [                            48.8316775417951            ],            [              0,              48.831550416507284            ],            [              0,              48.83168283867509            ],            [              0,              48.8316775417951            ]          ]        ]]}
Polygon003ha = {        "type": "MultiPolygon","coordinates": [  [          [            [              31.907668411731716,              48.8316775417951            ],            [              31.907770335674282,              48.831550416507284            ],            [              31.907781064510342,              48.83168283867509            ],            [              31.907668411731716,              48.8316775417951            ]          ]        ]]}
Polygons6 = {        "type": "MultiPolygon","coordinates":  [[          [            [              32.01021194458008,              48.80264841246314            ],            [              32.00985789299011,              48.802496480374224            ],            [              32.00992226600647,              48.80248588044387            ],            [              32.01044261455535,              48.802372814380675            ],            [              32.01021194458008,              48.80264841246314            ]          ]        ], [          [            [              32.010737657547,              48.80250708030235            ],            [              32.01064646244049,              48.802185548152856            ],            [              32.011274099349976,              48.80227034804076            ],            [              32.010737657547,              48.80250708030235            ]          ]        ], [          [            [              32.01089590787887,              48.80277384442227            ],            [              32.01099246740341,              48.80263074596481            ],            [              32.011349201202385,              48.80271201180556            ],            [              32.01089590787887,              48.80277384442227            ]          ]        ], [          [            [              32.01343059539795,              48.802999974485616            ],            [              32.013395726680756,              48.80268727873754            ],            [              32.013889253139496,              48.80290987591068            ],            [              32.01343059539795,              48.802999974485616            ]          ]        ], [          [            [              32.01373904943466,              48.80239224762843            ],            [              32.01392412185669,              48.8018375137778            ],            [              32.01472878456116,              48.802404614236714            ],            [              32.01373904943466,              48.80239224762843            ]          ]        ],[          [            [              31.959410905838013,              48.82151621240401            ],            [              31.961867809295658,              48.820272943673906            ],            [              31.96343421936035,              48.82210957978979            ],            [              31.959410905838013,              48.82151621240401            ]          ]        ]]}
Polygon1001ha ={        "type": "MultiPolygon","coordinates": [ [          [            [              31.9207763671875,              48.894066800857466            ],            [              31.94549560546875,              48.747587086042216            ],            [              32.2833251953125,              48.83489352771377            ],            [              31.9207763671875,              48.894066800857466            ]          ]        ]]}
Shape_geometry_empty = {        "type": "MultiPolygon","coordinates": [  [          [                      ]        ]]}
MultiPolygon_type_field = {        "type": "MultiPolygon","coordinates": [ [          [            [              31.9207763671875                          ]          ]        ]]}
