import unittest

from fastapi.testclient import TestClient

from api import app


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_predict(self) -> None:
        response = self.client.post("/predict", json={"word": "집", "pair": ["은", "는"]})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["selected_josa"], "은")
        self.assertEqual(body["combined_text"], "집은")

    def test_predict_invalid_request(self) -> None:
        response = self.client.post("/predict", json={"word": "", "pair": ["은", "는"]})
        self.assertEqual(response.status_code, 400)

    def test_predict_invalid_pair_length(self) -> None:
        response = self.client.post("/predict", json={"word": "집", "pair": ["은"]})
        self.assertEqual(response.status_code, 422)

    def test_predict_invalid_pair_value(self) -> None:
        response = self.client.post("/predict", json={"word": "집", "pair": ["은", " "]})
        self.assertEqual(response.status_code, 400)

    def test_predict_missing_pair_uses_default(self) -> None:
        response = self.client.post("/predict", json={"word": "집"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["selected_josa"], "은")


if __name__ == "__main__":
    unittest.main()
