from agents._common import run_points_agent
from config.prompts import SKEPTIC
from config.settings import POINTS


def skeptic_node(state):
    n = POINTS["opening"] if state["round"] == 1 else POINTS["rebuttal"]
    return run_points_agent("skeptic", "Skeptic", SKEPTIC, n, state)
