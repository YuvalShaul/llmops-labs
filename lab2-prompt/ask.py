"""The on-call assistant at its smallest: the system prompt from
system-prompt.txt, one question, one answer.

  python3 ask.py "A pod is in CrashLoopBackOff. What do I check first?"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import llm  # noqa: E402

PROMPT = Path(__file__).with_name("system-prompt.txt")


def answer(question):
    message, _ = llm.chat([
        {"role": "system", "content": PROMPT.read_text()},
        {"role": "user", "content": question},
    ])
    return message["content"].strip()


if __name__ == "__main__":
    print(answer(" ".join(sys.argv[1:]) or "A pod is in CrashLoopBackOff. What do I check first?"))
