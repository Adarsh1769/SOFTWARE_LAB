"""Check that the documented API contract matches the WSGI application."""

import io
import json
import unittest
from pathlib import Path

from app import application


API_DOCS = Path(__file__).with_name("API.md").read_text(encoding="utf-8")


def call_api(method, path, query="", body=None):
    if isinstance(body, bytes):
        raw_body = body
    else:
        raw_body = b"" if body is None else json.dumps(body).encode("utf-8")
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query,
        "CONTENT_LENGTH": str(len(raw_body)),
        "wsgi.input": io.BytesIO(raw_body),
    }
    result = {}

    def start_response(status, headers):
        result["status"] = status
        result["headers"] = dict(headers)

    response_body = b"".join(application(environ, start_response))
    result["body"] = json.loads(response_body.decode("utf-8"))
    return result


class ApiDocumentationTests(unittest.TestCase):
    def test_get_products_returns_documented_collection(self):
        response = call_api("GET", "/api/products")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(len(response["body"]["products"]), 3)
        self.assertIn("GET /api/products", API_DOCS)
        self.assertIn("200 OK", API_DOCS)

    def test_category_query_parameter_filters_case_insensitively(self):
        response = call_api("GET", "/api/products", "category=STATIONERY")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(
            [product["name"] for product in response["body"]["products"]],
            ["Notebook", "Pen"],
        )
        self.assertIn("`category`", API_DOCS)
        self.assertIn("case-insensitively", API_DOCS)

    def test_valid_post_returns_created_product(self):
        response = call_api(
            "POST",
            "/api/products",
            body={"name": "Bottle", "category": "home", "price": 12.5},
        )
        self.assertEqual(response["status"], "201 Created")
        self.assertEqual(response["body"]["product"]["name"], "Bottle")
        self.assertEqual(response["body"]["product"]["id"], 4)
        self.assertIn("POST /api/products", API_DOCS)
        self.assertIn("201 Created", API_DOCS)

    def test_invalid_post_returns_unprocessable_entity(self):
        response = call_api(
            "POST",
            "/api/products",
            body={"name": "", "category": "home", "price": -1},
        )
        self.assertEqual(response["status"], "422 Unprocessable Entity")
        self.assertIn("error", response["body"])
        self.assertIn("422 Unprocessable Entity", API_DOCS)

        malformed_json = call_api("POST", "/api/products", body=b"{invalid")
        self.assertEqual(malformed_json["status"], "422 Unprocessable Entity")
        self.assertEqual(malformed_json["body"], {"error": "Invalid JSON"})

    def test_unknown_route_returns_not_found(self):
        response = call_api("GET", "/api/unknown")
        self.assertEqual(response["status"], "404 Not Found")
        self.assertEqual(response["body"], {"error": "Route not found"})
        self.assertIn("404 Not Found", API_DOCS)


if __name__ == "__main__":
    unittest.main()
