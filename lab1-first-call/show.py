"""Read a model's JSON reply on standard input and print its answer, its
token counts and what the call would cost at example prices.

  curl ... | python3 show.py
"""

import json
import sys

# Example prices of a large hosted model, in dollars per million tokens.
PRICE_IN, PRICE_OUT = 3.00, 15.00

reply = json.load(sys.stdin)
answer = reply["choices"][0]["message"]["content"]
usage = reply["usage"]
tin, tout = usage["prompt_tokens"], usage["completion_tokens"]
cost = tin * PRICE_IN / 1e6 + tout * PRICE_OUT / 1e6

print(answer.strip())
print()
print(f"input tokens:  {tin}")
print(f"output tokens: {tout}")
print(f"cost at ${PRICE_IN:.2f} / ${PRICE_OUT:.2f} per million: ${cost:.6f}")
print(f"the same call 10,000 times a day: ${cost * 10_000:.2f} a day")
