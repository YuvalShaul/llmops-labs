"""The on-call assistant with retrieval: it cuts the runbooks into sections,
finds the sections nearest to the question, and sends them to the model
with the question.

  python3 ask.py "payments-api is slow. What do I check first?"          # the model alone
  python3 ask.py --rag "payments-api is slow. What do I check first?"    # with the runbooks
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import llm  # noqa: E402

RUNBOOKS = Path(__file__).with_name("runbooks")
TOP_K = 2

SYSTEM = "You are the on-call assistant of a DevOps team. Answer in at most four sentences."
SYSTEM_RAG = SYSTEM + (
    " Answer only from the runbook sections you are given, and name the file each step comes from."
    " If they do not cover the question, say so."
)


def chunks():
    """Each '## ' section of each runbook is one chunk, with its file and
    the runbook's title, so the chunk still makes sense on its own."""
    out = []
    for path in sorted(RUNBOOKS.glob("*.md")):
        title, heading, lines = "", "", []
        for line in path.read_text().splitlines() + ["## "]:
            if line.startswith("# "):
                title = line[2:]
            elif line.startswith("## "):
                if heading and lines:
                    out.append({"file": path.name, "text": f"{title} > {heading}\n" + "\n".join(lines).strip()})
                heading, lines = line[3:], []
            else:
                lines.append(line)
    return out


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def search(question):
    """The TOP_K chunks whose vectors are nearest to the question's."""
    found = chunks()
    vectors = llm.embed([c["text"] for c in found] + [question])
    q = vectors.pop()
    for c, v in zip(found, vectors):
        c["score"] = cosine(q, v)
    return sorted(found, key=lambda c: c["score"], reverse=True)[:TOP_K]


def main():
    args = sys.argv[1:]
    rag = "--rag" in args
    question = " ".join(a for a in args if a != "--rag") or "payments-api is slow. What do I check first?"

    if rag:
        best = search(question)
        print("Retrieved sections:")
        for c in best:
            print(f"  {c['score']:.3f}  {c['file']}: {c['text'].splitlines()[0]}")
        print()
        context = "\n\n".join(f'<source file="{c["file"]}">\n{c["text"]}\n</source>' for c in best)
        messages = [
            {"role": "system", "content": SYSTEM_RAG},
            {"role": "user", "content": f"Runbook sections:\n\n{context}\n\nQuestion: {question}"},
        ]
    else:
        messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]

    message, _ = llm.chat(messages)
    print(message["content"].strip())


if __name__ == "__main__":
    main()
