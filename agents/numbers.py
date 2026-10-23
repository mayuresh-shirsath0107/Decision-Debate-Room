from agents._common import run_points_agent
from config.prompts import NUMBERS
from config.settings import POINTS


def numbers_node(state):
    return run_points_agent("numbers", "Numbers", NUMBERS, POINTS["numbers"], state)
