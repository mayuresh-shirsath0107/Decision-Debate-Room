from agents._common import make_message
from config.prompts import JUDGE
from graph.state import Verdict
from utils.llm import get_llm


def judge_node(state):
    out = get_llm("judge", Verdict).invoke([("system", JUDGE), ("human", make_message(state))])
    verdict = out.model_dump()
    verdict["confidence"] = max(0, min(100, int(verdict["confidence"])))
    return {"verdict": verdict}
