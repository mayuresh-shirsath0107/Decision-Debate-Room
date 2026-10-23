"""Intake runs BEFORE the graph (it needs user input in the middle)."""
from config.prompts import INTAKE_QUESTIONS, INTAKE_BRIEF
from graph.state import Questions, Brief
from utils.llm import get_llm


def get_questions(decision: str) -> list[str]:
    out = get_llm("intake", Questions).invoke(
        [("system", INTAKE_QUESTIONS), ("human", f"Decision: {decision}")])
    return out.questions[:4]


def build_brief(decision: str, qa: list[tuple[str, str]]) -> str:
    answers = "\n".join(f"Q: {q}\nA: {a or 'not given'}" for q, a in qa)
    out = get_llm("intake", Brief).invoke(
        [("system", INTAKE_BRIEF), ("human", f"Decision: {decision}\n\n{answers}")])
    return out.brief
