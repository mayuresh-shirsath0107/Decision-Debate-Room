from agents._common import run_points_agent
from config.prompts import FUTURE_SELF
from config.settings import POINTS


def future_self_node(state):
    return run_points_agent("future_self", "Future Self", FUTURE_SELF, POINTS["future"], state)
