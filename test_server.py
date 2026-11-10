import unittest

import server


class ServerSecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = server.app.test_client()
        self.original_token = server.app.config["CYD_SERVER_TOKEN"]
        server.app.config["CYD_SERVER_TOKEN"] = "test-secret"
        with server._lock:
            server._messages.clear()

    def tearDown(self):
        server.app.config["CYD_SERVER_TOKEN"] = self.original_token
        with server._lock:
            server._messages.clear()

    def test_message_endpoints_require_bearer_token(self):
        for path, method in (
            ("/message", "post"),
            ("/messages", "get"),
            ("/messages/clear", "post"),
        ):
            with self.subTest(path=path):
                response = getattr(self.client, method)(path)
                self.assertEqual(response.status_code, 401)

    def test_unauthorized_clear_does_not_delete_messages(self):
        with server._lock:
            server._messages.append({"message": "keep me"})

        response = self.client.post("/messages/clear")

        self.assertEqual(response.status_code, 401)
        with server._lock:
            self.assertEqual(len(server._messages), 1)

    def test_bearer_token_allows_device_workflow(self):
        headers = {"Authorization": "Bearer test-secret"}
        response = self.client.post(
            "/message",
            json={"message": "hello", "source": "CYD"},
            headers=headers,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.get("/messages", headers=headers).get_json()["count"],
            1,
        )
        self.assertEqual(
            self.client.post("/messages/clear", headers=headers).status_code,
            200,
        )

    def test_liveness_routes_remain_public(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertEqual(self.client.get("/ping").status_code, 200)

    def test_oversized_request_body_is_rejected_as_json(self):
        response = self.client.post(
            "/message",
            data="x" * (server.MAX_REQUEST_BYTES + 1),
            content_type="application/json",
            headers={"Authorization": "Bearer test-secret"},
        )
        self.assertEqual(response.status_code, 413)
        self.assertFalse(response.get_json()["ok"])


if __name__ == "__main__":
    unittest.main()
