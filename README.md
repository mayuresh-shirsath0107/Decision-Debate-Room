# Decision Debate Room

A multi-agent AI system that helps you make everyday decisions. Instead of one AI giving one opinion, several AI agents debate your decision from different angles, and a Judge gives a final verdict with a confidence score.

---

## Problem

People usually decide using gut feeling or a one-sided pros-and-cons list. A single chatbot answer is often generic and tends to agree with whatever you already lean toward.

## Solution

Specialized agents argue for, against, and about the numbers of your decision, respond to each other, and imagine how you'll feel later. A Judge then weighs everything and recommends what to do.

## Agents

| Agent | Role |
|---|---|
| **Intake** | Asks a few clarifying questions and writes a short decision brief |
| **Optimist** | Argues the strongest case *for* the decision |
| **Skeptic** | Argues *against*: risks, hidden costs, regrets |
| **Numbers** | Analyzes money and measurable impact |
| **Future Self** | Describes how you'll feel in 1 month, 1 year and 5 years |
| **Judge** | Gives a recommendation, confidence %, deciding factors, risks and a first step |

## How the debate works

```
Intake -> Optimist -> Skeptic -> (rebuttal round) -> Numbers -> Future Self -> Judge
```

1. You describe your decision; Intake builds a brief.
2. **Round 1:** Optimist and Skeptic give 3 points each.
3. **Round 2:** each rebuts the other with 2 points.
4. Numbers and Future Self add their analysis (3 points each).
5. The Judge delivers the final verdict.

All agents share one state (the brief plus everything said so far), so each can respond to the others.

## Tech stack

- **Python 3.10+** for the logic
- **LangGraph** to connect the agents into a workflow
- **LangChain** model wrappers for Gemini, Groq and Cerebras
- **Pydantic** for structured agent outputs
- **Streamlit** for the web interface
- **uv** for fast dependency management

## Project structure

```
decision-debate-room/
├── main.py
├── app.py
├── pyproject.toml
├── .env
├── config/
│   ├── settings.py
│   └── prompts.py
├── agents/
│   ├── intake.py
│   ├── optimist.py
│   ├── skeptic.py
│   ├── numbers.py
│   ├── future_self.py
│   └── judge.py
├── graph/
│   ├── state.py
│   └── workflow.py
└── utils/
    └── llm.py
```

## Configuration

Everything adjustable lives in `config/settings.py`:

- **`ROUNDS`**: number of debate rounds (1 to 3)
- **`POINTS`**: points per agent (default 3 opening, 2 rebuttal)
- **`AGENT_MODELS`**: provider, model and temperature for each agent, plus a fallback model

Agent prompts are in `config/prompts.py`. Changing a model, round count or prompt never requires touching agent code.

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Install dependencies:
   ```
   uv sync
   ```
3. Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_gemini_key
   GROQ_API_KEY=your_groq_key
   CEREBRAS_API_KEY=your_cerebras_key
   ```
   You only need the keys for providers you actually use.
4. Open `config/settings.py` and set current model names. Names change often, so copy them from each provider's console. With only one key, point every agent and the fallback to that provider.

## Run

**Terminal:**
```
uv run python main.py
```
Saves each debate to a text file in `debates/`.

**Web UI:**
```
uv run streamlit run app.py
```
Shows each agent in its own chat bubble, a verdict card with a confidence bar, and a download button.

## Key features

- **Multi-agent debate** with real rebuttals, not just a list of points
- **Different model per agent**, chosen in one config file
- **Fallback model** if an agent's primary model fails or hits a limit
- **Structured outputs** so every provider returns the same format
- **Configurable** rounds, points, models and prompts
- **Modular**: add a new agent with one file and one line in the graph

## Troubleshooting

| Problem | Fix |
|---|---|
| `503 UNAVAILABLE` / high demand | Temporary provider overload. Retry, or make the fallback a different provider or model |
| `429` / quota exceeded | Free limit reached. Wait, or move that agent to another provider |
| `401` / key not found | Check the variable name and value in `.env` |
| `404` model not found | Model name changed. Update it in `config/settings.py` |
| `ModuleNotFoundError` | Run from the project root with `uv run` |

## Limitations and privacy

- It supports decisions and does not replace legal, medical or major financial advice.
- Outputs depend on the details you give, and models can be wrong or overconfident. The confidence score is an estimate.
- Free API tiers may log or use your inputs, so avoid sensitive personal details.
- Free tiers have rate limits, and some are for non-commercial use only.

## Future ideas

- Decision history and outcome tracking
- Shareable verdict cards
- Adjustable agent personalities
- Extra agents, such as a "Family opinion" or "Risk-taker" agent