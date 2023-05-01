from tests import BaseTestCase

from engin.server.app import app


class SanicHealthTestCase(BaseTestCase):
    def test_get(self):
        request, response = app.test_client.get("/health")

        assert request.method.lower() == "get"
        assert response.body == b"Pong!"
        assert response.status == 200
