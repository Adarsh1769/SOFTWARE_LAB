"""A small WSGI API used to demonstrate generated API documentation."""

import json
import math
from urllib.parse import parse_qs


PRODUCTS = [
    {"id": 1, "name": "Notebook", "category": "stationery", "price": 4.5},
    {"id": 2, "name": "Pen", "category": "stationery", "price": 1.25},
    {"id": 3, "name": "Mug", "category": "home", "price": 8.0},
]


def _respond(start_response, status, payload):
    body = json.dumps(payload).encode("utf-8")
    start_response(
        status,
        [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]


def application(environ, start_response):
    """Handle GET /api/products and POST /api/products requests."""
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    if path != "/api/products":
        return _respond(
            start_response, "404 Not Found", {"error": "Route not found"}
        )

    if method == "GET":
        query = parse_qs(environ.get("QUERY_STRING", ""))
        category = query.get("category", [None])[0]
        products = PRODUCTS
        if category:
            products = [
                product
                for product in PRODUCTS
                if product["category"].casefold() == category.casefold()
            ]
        return _respond(start_response, "200 OK", {"products": products})

    if method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH") or "0")
        except ValueError:
            return _respond(
                start_response, "400 Bad Request", {"error": "Invalid content length"}
            )
        body = environ["wsgi.input"].read(content_length)
        try:
            payload = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return _respond(
                start_response, "422 Unprocessable Entity", {"error": "Invalid JSON"}
            )

        if not isinstance(payload, dict):
            return _respond(
                start_response,
                "422 Unprocessable Entity",
                {"error": "Request body must be a JSON object"},
            )
        name = payload.get("name")
        category = payload.get("category")
        price = payload.get("price")
        if (
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(category, str)
            or not category.strip()
            or isinstance(price, bool)
            or not isinstance(price, (int, float))
            or not math.isfinite(price)
            or price <= 0
        ):
            return _respond(
                start_response,
                "422 Unprocessable Entity",
                {
                    "error": (
                        "name and category must be non-empty strings; "
                        "price must be a positive number"
                    )
                },
            )

        created = {
            "id": len(PRODUCTS) + 1,
            "name": name.strip(),
            "category": category.strip(),
            "price": price,
        }
        return _respond(start_response, "201 Created", {"product": created})

    return _respond(
        start_response,
        "405 Method Not Allowed",
        {"error": "Method not allowed"},
    )


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    with make_server("127.0.0.1", 8000, application) as server:
        print("Serving API at http://127.0.0.1:8000")
        server.serve_forever()
