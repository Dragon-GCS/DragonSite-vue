import unittest
from urllib import response
from server import app
from fastapi.testclient import TestClient

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_get_resource(self):
        response = self.client.get("/api/disk?path=/&filter=all")
        print(response)
        print(response.json())
        # self.assertEqual(response.url, "http://testserver/home")

    def test_post_resource(self):
        response = self.client.post("/api/disk?path=/&is_dir=true&name=test")
        print(response)
        print(response.json())


if __name__ == '__main__':
    unittest.main()