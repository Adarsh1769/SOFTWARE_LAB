"""Generate API.md from app.py with a locally running Ollama model."""

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HERE = Path(__file__).resolve().parent
SOURCE_FILE = HERE / "app.py"
OUTPUT_FILE = HERE / "API.md"


def main():
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    source = SOURCE_FILE.read_text(encoding="utf-8")
    prompt = f"""Write concise Markdown API documentation based only on this Python
WSGI source. Include each route, method, query parameter, request/response JSON,
HTTP status code, validation rule, and whether created products are persisted.
Do not claim behavior that is not present in the code. Return only Markdown.

Source:
```python
{source}
```"""
    request = Request(
        f"{host}/api/generate",
        data=json.dumps(
            {"model": model, "prompt": prompt, "stream": False}
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as error:
        raise SystemExit(
            f"Could not reach Ollama at {host}. Start Ollama and pull {model}: {error}"
        ) from error

    documentation = result.get("response", "").strip()
    if not documentation:
        raise SystemExit("Ollama returned empty documentation.")
    OUTPUT_FILE.write_text(documentation + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT_FILE.name} with Ollama model {model}.")


if __name__ == "__main__":
    main()
