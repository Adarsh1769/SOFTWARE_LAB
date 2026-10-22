"""Unstructured legacy-style order summary used as the refactoring source."""


def process(data):
    s = 0
    n = 0
    for x in data:
        if len(x) > 2:
            q = x[1]
            p = x[2]
            if q > 0 and p >= 0:
                z = q * p
                if z > 100:
                    z = z * 0.9
                s = s + z
                n = n + q
    if n > 0:
        a = s / n
    else:
        a = 0
    return {"total": round(s, 2), "units": n, "average": round(a, 2)}


if __name__ == "__main__":
    sample_orders = [
        ("Notebook", 2, 25.00),
        ("Desk", 1, 150.00),
        ("Invalid quantity", 0, 12.00),
    ]
    print(process(sample_orders))
