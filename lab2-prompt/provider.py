"""promptfoo's way into our application: it calls call_api() once per test
case, and we answer through ask.py, so the eval tests the assistant as it
runs, with its system prompt, and not a bare model."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ask import answer  # noqa: E402


def call_api(prompt, options, context):
    return {"output": answer(prompt)}
