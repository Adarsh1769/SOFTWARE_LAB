# Products API

Base URL: `http://127.0.0.1:8000`

## `GET /api/products`

Returns the sample products as `{"products": [...]}` with **200 OK**.

Optional query parameter:

| Name | Type | Description |
|---|---|---|
| `category` | string | Filters products by category, case-insensitively. |

An unknown route returns **404 Not Found** with `{"error": "Route not found"}`.

## `POST /api/products`

Creates and returns a product with **201 Created**:

```json
{
  "name": "Bottle",
  "category": "home",
  "price": 12.5
}
```

`name` and `category` must be non-empty strings. `price` must be a positive
number (not a boolean). A malformed JSON body or invalid fields return
**422 Unprocessable Entity** with an `error` message. The example returns a
created product with an ID but does not persist it.

Other HTTP methods return **405 Method Not Allowed**.
