"""The labs' one connection to a model: an OpenAI-compatible API, called with
Python's standard library only, so the labs need no pip install.

Three environment variables choose the model; the defaults are Ollama on
this machine (see the first lab's setup):

  LLM_BASE_URL     http://localhost:11434/v1
  LLM_API_KEY      none   (Ollama ignores it; a gateway needs a real key)
  LLM_MODEL        qwen2.5:3b
  LLM_EMBED_MODEL  nomic-embed-text
  LLM_SEED         1
"""

import json
import os
import urllib.error
import urllib.request

BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1").rstrip("/")
API_KEY = os.environ.get("LLM_API_KEY", "none")
MODEL = os.environ.get("LLM_MODEL", "qwen2.5:3b")
EMBED_MODEL = os.environ.get("LLM_EMBED_MODEL", "nomic-embed-text")
SEED = int(os.environ.get("LLM_SEED", "1"))


def post(path, body):
    """POST a JSON body to the API and return the JSON reply."""
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        raise SystemExit(f"The model's API refused the call: HTTP {err.code}\n{err.read().decode()}")
    except urllib.error.URLError as err:
        raise SystemExit(f"No model's API answers at {BASE_URL}: {err.reason}\nIs Ollama running? See the first lab's setup.")


def chat(messages, tools=None, temperature=0):
    """One call to the model: the messages so far in, the reply message out."""
    # A fixed seed makes a run repeatable: the same question takes the same
    # path every time, on the same model.
    body = {"model": MODEL, "messages": messages, "temperature": temperature, "seed": SEED}
    if tools:
        body["tools"] = tools
    reply = post("/chat/completions", body)
    return reply["choices"][0]["message"], reply.get("usage", {})


def embed(texts):
    """One semantic vector per text."""
    reply = post("/embeddings", {"model": EMBED_MODEL, "input": texts})
    return [item["embedding"] for item in reply["data"]]
