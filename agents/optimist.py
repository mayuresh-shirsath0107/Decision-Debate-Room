from agents._common import run_points_agent
from config.prompts import OPTIMIST
from config.settings import POINTS


def optimist_node(state):
    n = POINTS["opening"] if state["round"] == 1 else POINTS["rebuttal"]
    return run_points_agent("optimist", "Optimist", OPTIMIST, n, state)
