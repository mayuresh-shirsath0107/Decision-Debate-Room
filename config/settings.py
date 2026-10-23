"""All tunable settings live here. Change models/rounds/points without touching agent code.

NOTE: model names change often. Check each provider's console and update them here.
If you only have ONE key, set every agent (and the fallback) to that provider.
Providers supported: "gemini", "groq", "cerebras"
"""

ROUNDS = 2  # round 1 = opening arguments, round 2 = rebuttals (set 1 to 3)

POINTS = {"opening": 3, "rebuttal": 2, "numbers": 3, "future": 3}

AGENT_MODELS = {
    "intake":      {"provider": "groq",   "model": "openai/gpt-oss-120b", "temperature": 0.4},
    "optimist":    {"provider": "groq",   "model": "openai/gpt-oss-120b", "temperature": 0.8},
    "skeptic":     {"provider": "groq",   "model": "openai/gpt-oss-120b",      "temperature": 0.7},
    "numbers":     {"provider": "gemini", "model": "gemini-3.8-flash",        "temperature": 0.2},
    "future_self": {"provider": "gemini", "model": "gemini-3.8-flash",        "temperature": 0.9},
    "judge":       {"provider": "gemini", "model": "gemini-3.8-flash",        "temperature": 0.3},
    # Used automatically if an agent's primary model fails (rate limit, outage)
    "fallback":    {"provider": "groq",   "model": "openai/gpt-oss-120b", "temperature": 0.5},
}

# Display info (used by terminal and Streamlit)
AGENT_DISPLAY = {
    "optimist":    {"name": "Optimist",    "emoji": "🟢"},
    "skeptic":     {"name": "Skeptic",     "emoji": "🔴"},
    "numbers":     {"name": "Numbers",     "emoji": "🔢"},
    "future_self": {"name": "Future Self", "emoji": "🔮"},
    "judge":       {"name": "Judge",       "emoji": "⚖️"},
}
