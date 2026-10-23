"""LangGraph workflow: optimist -> skeptic -> (loop for ROUNDS) -> numbers -> future_self -> judge."""
from langgraph.graph import StateGraph, START, END

from agents.future_self import future_self_node
from agents.judge import judge_node
from agents.numbers import numbers_node
from agents.optimist import optimist_node
from agents.skeptic import skeptic_node
from config.settings import ROUNDS
from graph.state import DebateState


def next_round_or_experts(state) -> str:
    return "again" if state["round"] < ROUNDS else "done"


def bump_round(state):
    return {"round": state["round"] + 1}


def initial_state(decision: str, brief: str) -> dict:
    return {"decision": decision, "brief": brief, "round": 1, "arguments": [], "verdict": {}}


def build_graph():
    g = StateGraph(DebateState)
    g.add_node("optimist", optimist_node)
    g.add_node("skeptic", skeptic_node)
    g.add_node("bump_round", bump_round)
    g.add_node("numbers", numbers_node)
    g.add_node("future_self", future_self_node)
    g.add_node("judge", judge_node)

    g.add_edge(START, "optimist")
    g.add_edge("optimist", "skeptic")
    g.add_conditional_edges("skeptic", next_round_or_experts,
                            {"again": "bump_round", "done": "numbers"})
    g.add_edge("bump_round", "optimist")
    g.add_edge("numbers", "future_self")
    g.add_edge("future_self", "judge")
    g.add_edge("judge", END)
    return g.compile()
