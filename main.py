"""Terminal version. Run with:  uv run python main.py"""
import os
from datetime import datetime

from agents.intake import build_brief, get_questions
from config.settings import AGENT_DISPLAY, ROUNDS
from graph.workflow import build_graph, initial_state


def format_verdict(v: dict) -> str:
    lines = ["", "=" * 60, "  FINAL VERDICT", "=" * 60,
             f"Recommendation : {v['recommendation']}",
             f"Confidence     : {v['confidence']}%", "", "Deciding factors:"]
    lines += [f"  {i}. {x}" for i, x in enumerate(v["deciding_factors"], 1)]
    lines += ["", "Risks to watch:"] + [f"  - {x}" for x in v["risks"]]
    lines += ["", f"First step today: {v['first_step']}", "=" * 60]
    return "\n".join(lines)


def main():
    print("\n=== Decision Debate Room ===\n")
    decision = input("What decision are you facing?\n> ").strip()
    if not decision:
        return

    print("\nA few quick questions so the debate is specific:\n")
    qa = []
    for q in get_questions(decision):
        qa.append((q, input(f"{q}\n> ").strip()))
    brief = build_brief(decision, qa)
    print(f"\nDecision brief:\n{brief}\n")

    transcript = [f"DECISION BRIEF\n{brief}\n"]
    app = build_graph()
    key_for = {"optimist": "optimist", "skeptic": "skeptic", "numbers": "numbers",
               "future_self": "future_self"}
    round_no = 1
    for update in app.stream(initial_state(decision, brief), stream_mode="updates"):
        for node, data in update.items():
            if node == "bump_round":
                round_no = data["round"]
            elif node in key_for:
                a = data["arguments"][0]
                d = AGENT_DISPLAY[node]
                tag = f"Round {a['round']}/{ROUNDS}" if node in ("optimist", "skeptic") else "Expert"
                block = f"\n{d['emoji']} {d['name']} ({tag})\n" + "\n".join(f"  - {p}" for p in a["points"])
                print(block); transcript.append(block)
            elif node == "judge":
                text = format_verdict(data["verdict"])
                print(text); transcript.append(text)

    os.makedirs("debates", exist_ok=True)
    path = os.path.join("debates", f"debate_{datetime.now():%Y%m%d_%H%M%S}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(transcript))
    print(f"\nSaved to {path}")


if __name__ == "__main__":
    main()
