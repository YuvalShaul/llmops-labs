# LLMOps labs

The data and code of the labs of [LLMOps for AI Agents](https://www.yuval.guide/llmops/llmops-top/).
The instructions are on the site, one post per lab:

| Directory | Lab |
| --- | --- |
| `lab1-first-call/` | [Lab 1: One Call to a Model](https://www.yuval.guide/llmops/llmops-lab-1-first-call/) |
| `lab2-prompt/` | [Lab 2: A Prompt in Git, Tested](https://www.yuval.guide/llmops/llmops-lab-2-prompt/) |
| `lab3-runbooks/` | [Lab 3: Answers from Our Runbooks](https://www.yuval.guide/llmops/llmops-lab-3-runbooks/) |
| `lab4-agent/` | [Lab 4: A Small Agent, and an Attack on It](https://www.yuval.guide/llmops/llmops-lab-4-agent/) |

- `llm.py` is the labs' one connection to a model: an OpenAI-compatible API, called with Python's standard library.
- `.github/workflows/prompt-check.yml` runs lab 2's eval on every pull request that changes the prompt.

Use this repository as a template: **Use this template → Create a new repository**, then clone your copy.
