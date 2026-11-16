"""The on-call assistant as an agent: the model chooses which tool to call,
and this code runs it.

  python3 agent.py "Check the payments pods, and open a ticket for each problem a person must fix."

The two read tools read a saved snapshot of a cluster (the files in
cluster/), so the lab needs no cluster; a real agent would run kubectl.
The one write tool, open_ticket, asks you before it runs.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import llm  # noqa: E402

CLUSTER = Path(__file__).with_name("cluster")
MAX_TURNS = 6          # a run that reaches it stops
TICKETS = Path(__file__).with_name("tickets.txt")

SYSTEM = (
    "You are the on-call assistant of a DevOps team. "
    "Use the tools to look at the cluster before you answer: "
    "call get_pods, then get_logs on the failing pod, and keep calling tools until you know the cause. "
    "Never write that you will check something: call the tool instead. "
    "When you know the cause, answer in at most four sentences. "
    "Open a ticket only when a person must fix something."
)

TOOLS = [
    {"type": "function", "function": {
        "name": "get_pods",
        "description": "List the pods in the cluster with their status and restarts. Use it first, to see what is wrong.",
        "parameters": {"type": "object", "properties": {}},
    }},
    {"type": "function", "function": {
        "name": "get_logs",
        "description": "Read the recent log lines of one pod. Use it to find why a pod fails.",
        "parameters": {"type": "object", "properties": {
            "pod": {"type": "string", "description": "The pod's full name, as get_pods lists it."}},
            "required": ["pod"]},
    }},
    {"type": "function", "function": {
        "name": "open_ticket",
        "description": "Open a ticket for the team. Use it only when a person must fix something.",
        "parameters": {"type": "object", "properties": {
            "title": {"type": "string", "description": "One line saying what is wrong."},
            "severity": {"type": "string", "enum": ["low", "high", "urgent"]}},
            "required": ["title", "severity"]},
    }},
]


def get_pods():
    return (CLUSTER / "pods.txt").read_text()


def get_logs(pod):
    path = CLUSTER / "logs" / f"{Path(pod).name}.log"
    return path.read_text() if path.exists() else f"No pod named {pod}."


def open_ticket(title, severity):
    """The write tool: it runs only after a person approves it."""
    print(f"\n  The agent asks to open a ticket:\n    title:    {title}\n    severity: {severity}")
    if input("  Approve? [y/N] ").strip().lower() != "y":
        return "A person rejected this ticket. Do not open it again."
    with TICKETS.open("a") as f:
        f.write(f"[{severity}] {title}\n")
    return "Ticket opened."


RUN = {"get_pods": get_pods, "get_logs": get_logs, "open_ticket": open_ticket}


def main():
    question = " ".join(sys.argv[1:]) or "Check the payments pods, and open a ticket for each problem a person must fix."
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    total_in = total_out = 0

    for turn in range(1, MAX_TURNS + 1):
        message, usage = llm.chat(messages, tools=TOOLS)
        total_in += usage.get("prompt_tokens", 0)
        total_out += usage.get("completion_tokens", 0)
        messages.append(message)
        calls = message.get("tool_calls") or []

        if not calls:
            print(f"\nTurn {turn}: the answer\n{(message.get('content') or '').strip()}")
            break
        for call in calls:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            args = json.loads(args) if isinstance(args, str) else (args or {})
            print(f"Turn {turn}: {name}({', '.join(f'{k}={v!r}' for k, v in args.items())})")
            result = RUN[name](**args) if name in RUN else f"No tool named {name}."
            messages.append({"role": "tool", "tool_call_id": call.get("id", name), "content": result})
    else:
        print(f"\nStopped: the run reached its limit of {MAX_TURNS} turns.")

    print(f"\n{turn} model calls, {total_in} input tokens, {total_out} output tokens")


if __name__ == "__main__":
    main()
