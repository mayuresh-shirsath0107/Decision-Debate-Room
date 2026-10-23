"""Helpers shared by the point-making agents (kept tiny so each agent file stays simple)."""
from graph.state import Points
from utils.llm import get_llm


def format_arguments(state) -> str:
    lines = []
    for a in state["arguments"]:
        pts = " | ".join(a["points"])
        lines.append(f"[Round {a['round']}] {a['agent']}: {pts}")
    return "\n".join(lines) or "(nothing yet)"


def make_message(state) -> str:
    return (
        f"DECISION BRIEF:\n{state['brief']}\n\n"
        f"DEBATE SO FAR:\n{format_arguments(state)}\n\n"
        f"This is round {state['round']}. Do not repeat earlier points."
    )


def run_points_agent(key: str, label: str, system_prompt: str, n: int, state) -> dict:
    out = get_llm(key, Points).invoke([("system", system_prompt.format(n=n)),
                                       ("human", make_message(state))])
    return {"arguments": [{"agent": label, "round": state["round"], "points": out.points}]}
