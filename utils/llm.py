"""One function used by every agent to get its model (with structured output + fallback)."""
from dotenv import load_dotenv
from config.settings import AGENT_MODELS

load_dotenv()


def _build(provider: str, model: str, temperature: float):
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model, temperature=temperature)
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model=model, temperature=temperature)
    if provider == "cerebras":
        from langchain_cerebras import ChatCerebras
        return ChatCerebras(model=model, temperature=temperature)
    raise ValueError(f"Unknown provider: {provider}")


def get_llm(agent: str, schema):
    """Return a runnable that outputs `schema`, falling back to the backup model on errors."""
    c, f = AGENT_MODELS[agent], AGENT_MODELS["fallback"]
    primary = _build(c["provider"], c["model"], c["temperature"]).with_structured_output(schema, method="json_mode")
    backup = _build(f["provider"], f["model"], f["temperature"]).with_structured_output(schema, method="json_mode")
    return primary.with_fallbacks([backup])
