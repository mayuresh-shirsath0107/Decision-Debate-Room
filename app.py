"""Streamlit UI. Run with:  uv run streamlit run app.py"""
import streamlit as st

from agents.intake import build_brief
from config.settings import AGENT_DISPLAY, ROUNDS
from graph.workflow import build_graph, initial_state

st.set_page_config(page_title="Decision Debate Room", page_icon="⚖️")
st.title("⚖️ Decision Debate Room")
st.caption("Describe a tough decision. AI agents debate it and a Judge gives a verdict. "
           "Tip: avoid sensitive personal details; free-tier models may log inputs.")

decision = st.text_area("What decision are you facing?",
                        placeholder="Should I accept a job offer in Pune with a 30% raise but higher rent?")
c1, c2 = st.columns(2)
money = c1.text_input("Budget / money situation (optional)")
priority = c2.text_input("What matters most to you? (optional)")
deadline = st.text_input("Deadline to decide (optional)")

if st.button("Start the debate", type="primary"):
    if not decision.strip():
        st.warning("Please describe your decision first.")
        st.stop()

    transcript = []
    try:
        with st.spinner("Preparing the brief..."):
            brief = build_brief(decision, [("Budget / money situation?", money),
                                           ("What matters most?", priority),
                                           ("Deadline?", deadline)])
        st.info(f"**Decision brief**\n\n{brief}")
        transcript.append(f"DECISION BRIEF\n{brief}\n")

        app = build_graph()
        for update in app.stream(initial_state(decision, brief), stream_mode="updates"):
            for node, data in update.items():
                if node in ("optimist", "skeptic", "numbers", "future_self"):
                    a, d = data["arguments"][0], AGENT_DISPLAY[node]
                    tag = f"Round {a['round']}/{ROUNDS}" if node in ("optimist", "skeptic") else "Expert opinion"
                    with st.chat_message(d["name"], avatar=d["emoji"]):
                        st.markdown(f"**{d['name']}** - {tag}")
                        for p in a["points"]:
                            st.markdown(f"- {p}")
                    transcript.append(f"{d['name']} ({tag})\n" + "\n".join(f"- {p}" for p in a["points"]))
                elif node == "judge":
                    v = data["verdict"]
                    st.subheader("⚖️ Final verdict")
                    st.success(f"**{v['recommendation']}**")
                    st.progress(v["confidence"] / 100, text=f"Confidence: {v['confidence']}%")
                    st.markdown("**Deciding factors**")
                    for x in v["deciding_factors"]:
                        st.markdown(f"- {x}")
                    st.markdown("**Risks to watch**")
                    for x in v["risks"]:
                        st.markdown(f"- {x}")
                    st.markdown(f"**First step today:** {v['first_step']}")
                    transcript.append(f"VERDICT: {v}")
        st.download_button("Download full debate", "\n\n".join(transcript), file_name="debate.txt")
    except Exception as e:
        st.error(f"Something went wrong: {e}. Check your API keys in .env and model names in config/settings.py.")
