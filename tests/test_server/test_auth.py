import unittest

from fastapi.testclient import TestClient

from server import app

from . import TEST_USER


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app, base_url="http://testserver/api/auth")

    def test_login(self):
        response = self.client.post("login", data=TEST_USER.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "login"})
        self.assertEqual(response.cookies.get("username"), TEST_USER.username)
        expired_time = int(response.cookies.get("expired_time") or 0)
        entropy_password = TEST_USER.encrypt_password(TEST_USER.password)
        self.assertEqual(
            response.cookies.get("token"), TEST_USER.generate_token(expired_time, entropy_password)
        )

    def test_invalid_user(self):
        response = self.client.post("login", data={"username": "user1", "password": "testpassword"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Authentication failed"})

    def test_invalid_password(self):
        response = self.client.post(
            "login", data={"username": TEST_USER.username, "password": "password1"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Authentication failed"})

    def test_logout(self):
        try:
            self.client.post("login", data=TEST_USER.dict())
        except Exception as e:
            raise unittest.SkipTest(str(e)) from e

        self.assertIsNotNone(self.client.cookies.get("token"))
        response = self.client.post("logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "logout"})
        self.assertIsNone(self.client.cookies.get("token"))
