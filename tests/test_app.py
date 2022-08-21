from flask_testing import TestCase
from db import db
from config import create_app
from models import AnalystsModel, UserRole

ENDPOINTS_DATA = (
    ("/recommendation?ticker=amzn", "GET"),
    ("/analysis?ticker=amzn", "GET"),
    ("/balancesheet?ticker=amzn", "GET"),
    ("/view_my_analysis", "GET"),

)

class TestApp(TestCase):

    def create_app(self):
        return create_app("config.TestApplicationConfiguration")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def iterate_endpoints(
            self,
            endpoints_data,
            status_code_method,
            expected_resp_body,
            headers=None,
            payload=None,
    ):
        if not headers:
            headers = {}
        if not payload:
            payload = {}

        resp = None
        for url, method in endpoints_data:
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "POST":
                resp = self.client.post(url, headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)
            status_code_method(resp)
            self.assertEqual(resp.json, expected_resp_body)

    def test_invalid_token_raises(self):
        headers = {"Authorization": "Bearer eyJ0eX"}
        self.iterate_endpoints(
            ENDPOINTS_DATA, self.assert_401, None, headers
        )

    def test_login_required(self):
        self.iterate_endpoints(
            ENDPOINTS_DATA, self.assert_401, None
        )

    def test_user_journey(self):

        payload = {
            "first_name": "Peter",
            "last_name": "Ivanov",
            "email": "pesho@ivanov.bg",
            "password": "12345678kK"
        }
        headers = {
            'Content-Type': 'application/json'
        }

        resp = self.client.post('/register', headers=headers, json=payload)
        self.assert_status(status_code=201, response=resp)
        token = resp.json['token']
        headers = {"Authorization": f"Bearer {token}"}
        for endpoint, method in ENDPOINTS_DATA:
            resp = self.client.get(endpoint, headers=headers)
            if any(x in endpoint for x in ['recommendation', 'view_my_analysis']):
                self.assert_status(status_code=200, response=resp)
            else:
                self.assert_status(status_code=403, response=resp)

    def test_user_journey_premium(self):

        payload = {
            "first_name": "Peter",
            "last_name": "Ivanov",
            "email": "pesho@ivanov.bg",
            "password": "12345678kK"
        }
        headers = {
            'Content-Type': 'application/json'
        }

        resp = self.client.post('/register', headers=headers, json=payload)
        self.assert_status(status_code=201, response=resp)
        token = resp.json['token']

        user_id = AnalystsModel.decode_token(token=token)
        user = AnalystsModel.query.filter_by(id=user_id).first()
        user.role = UserRole.Premium
        db.session.commit()
        headers = {"Authorization": f"Bearer {token}"}
        for endpoint, method in ENDPOINTS_DATA:
            resp = self.client.get(endpoint, headers=headers)
            self.assert_status(status_code=200, response=resp)

    def test_user_dupliation(self):

        payload = {
            "first_name": "Peter",
            "last_name": "Ivanov",
            "email": "pesho@ivanov.bg",
            "password": "12345678kK"
        }
        headers = {
            'Content-Type': 'application/json'
        }

        resp = self.client.post('/register', headers=headers, json=payload)
        self.assert_status(status_code=201, response=resp)

        resp = self.client.post('/register', headers=headers, json=payload)
        self.assert_status(status_code=409, response=resp)
        self.assertEqual(resp.json, {"message": "User already exists!"})

    def test_login_functionality(self):

        payload = {
            "first_name": "Peter",
            "last_name": "Ivanov",
            "email": "pesho@ivanov.bg",
            "password": "12345678kK"
        }
        headers = {
            'Content-Type': 'application/json'
        }

        resp = self.client.post('/register', headers=headers, json=payload)
        self.assert_status(status_code=201, response=resp)

        del payload['first_name']
        del payload['last_name']

        resp = self.client.post('/login', headers=headers, json=payload)
        self.assert_status(status_code=200, response=resp)












