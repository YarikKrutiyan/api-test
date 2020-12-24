from api.auth.api_authorization import authorization
from src.config import USER


class TestAuthorization:

    def test_authorization_positive(self, hosts):
        auth = authorization(hosts['endpoint'],USER)

        print(auth.json())
        assert auth.status_code == 200, 'Failed to login'
        assert auth.json()['token'] is not None, 'Missing token'
        assert auth.json()['refresh_token'] is not None, 'Missing refresh_token'
        assert auth.json()['token'] != auth.json()['refresh_token'], 'Token and refreshtoken are the same'

    def test_authorization_no_valid_email(self, hosts):
        authorization_no_valid_email = USER.copy()
        authorization_no_valid_email['email'] = "eewwe"
        auth = authorization(hosts['endpoint'], authorization_no_valid_email)
        assert auth.status_code == 400, 'Auth withut email'
        assert auth.json()['errors']['email'][0] == 2003, "code of errors email is not valid"

    def test_authorization_no_valid_password(self, hosts):
        authorization_no_valid_password = USER.copy()
        authorization_no_valid_password['password'] = "e11we"
        auth = authorization(hosts['endpoint'], authorization_no_valid_password)
        assert auth.status_code == 400, 'Auth withut password'
        assert auth.json()['errors']['password'][0] == 2004, "code of errors email is not password"

    def test_authorization_no_email(self, hosts):
        authorization_no_email = USER.copy()
        authorization_no_email['email'] = ""
        auth = authorization(hosts['endpoint'], authorization_no_email)
        assert auth.status_code == 400, 'Auth withut email'
        assert auth.json()['errors']['email'][0] == 2003, "code of errors email is not valid"

    def test_authorization_no_valid_email(self, hosts):
        authorization_no_valid_email = USER.copy()
        authorization_no_valid_email['email'] = "eewwe"
        auth = authorization(hosts['endpoint'], authorization_no_valid_email)
        assert auth.status_code == 400, 'Auth without email'
        assert auth.json()['errors']['email'][0] == 2003, "code of errors email is not valid"

    def test_authorization_no_valid_password(self, hosts):
        authorization_no_valid_password = USER.copy()
        authorization_no_valid_password['password'] = "e11we"
        auth = authorization(hosts['endpoint'], authorization_no_valid_password)
        assert auth.status_code == 400, 'Auth without password'
        assert auth.json()['errors']['email'][0] == 2005, "code of errors email is not password"

    def test_authorization_no_email(self, hosts):
        authorization_no_email = USER.copy()
        authorization_no_email['email'] = ""
        auth = authorization(hosts['endpoint'], authorization_no_email)
        assert auth.status_code == 400, 'Auth without email'
        assert auth.json()['errors']['email'][0] == 2003, "code of errors email is not valid"

    def test_authorization_no_password(self, hosts):
        authorization_no_password = USER.copy()
        authorization_no_password['password'] = ""
        auth = authorization(hosts['endpoint'], authorization_no_password)
        assert auth.status_code == 400, 'Auth without password'
        assert auth.json()['errors']['password'][0] == 2004, "code of errors password is not valid"

    def test_authorization_no_password_email(self, hosts):
        authorization_no_password = USER.copy()
        authorization_no_password['password'] = ""
        authorization_no_password['email'] = ""
        auth = authorization(hosts['endpoint'], authorization_no_password)
        assert auth.status_code == 400, 'Auth without email&password'
        assert auth.json()['errors']['password'][0] == 2004,  "code of errors email&password is not valid"
