"""
DataOps Copilot - Streamlit UI.

A conversational front end over the FastAPI service (api.py). Lets a data
engineer ask for an investigation, review the evidence-backed summary, and
trigger remediation with an explicit confirmation step.

Run (with the API already running on :8000):
    uvicorn api:app --reload &
    streamlit run streamlit_app.py
"""
import os
import requests
import streamlit as st

API_URL = os.environ.get("DATAOPS_API_URL", "http://localhost:8000")

st.set_page_config(page_title="DataOps Copilot", page_icon="🛠️", layout="wide")
st.title("🛠️ DataOps Copilot")
st.caption(
    "AI-powered data-quality investigation and remediation — every claim below "
    "is grounded in a deterministic tool call, never invented."
)

with st.sidebar:
    st.subheader("Backend status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=5).json()
        st.success("API reachable")
        st.json(health)
    except Exception as e:
        st.error(f"Cannot reach API at {API_URL}: {e}")
        st.info("Start it with: uvicorn api:app --reload")

    st.subheader("Live quality status")
    if st.button("Refresh status"):
        st.session_state["status"] = requests.get(f"{API_URL}/quality/status", timeout=10).json()
    if "status" not in st.session_state:
        try:
            st.session_state["status"] = requests.get(f"{API_URL}/quality/status", timeout=10).json()
        except Exception:
            st.session_state["status"] = None
    if st.session_state.get("status"):
        s = st.session_state["status"]
        st.metric("Total records", s.get("total_records"))
        st.metric("Status", s.get("status"))
        col1, col2, col3 = st.columns(3)
        col1.metric("NULL ids", s.get("null_customer_id_count"))
        col2.metric("Duplicates", s.get("duplicate_count"))
        col3.metric("Invalid emails", s.get("invalid_email_count"))
        if s.get("issues"):
            st.warning("\n".join(s["issues"]))

st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "last_evidence" not in st.session_state:
    st.session_state["last_evidence"] = None

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask the Copilot to investigate, e.g. 'Investigate the customer dataset for quality issues'")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Running diagnostic tools..."):
            try:
                resp = requests.post(f"{API_URL}/investigate", json={"request": prompt}, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                st.markdown(data.get("summary", "(no summary returned)"))
                with st.expander("Evidence (raw tool output)"):
                    st.json(data.get("evidence"))
                st.session_state["last_evidence"] = data.get("evidence")
                st.session_state["messages"].append({"role": "assistant", "content": data.get("summary", "")})
            except Exception as e:
                st.error(f"Investigation failed: {e}")

st.divider()
st.subheader("Remediation")
st.caption("Runs quarantine_invalid_records -> create_cleaned_dataset -> verify_cleaned_dataset.")
confirm = st.checkbox("I confirm I want to quarantine invalid records and build a cleaned dataset.")
if st.button("Run remediation", type="primary", disabled=not confirm):
    with st.spinner("Remediating..."):
        try:
            resp = requests.post(f"{API_URL}/remediate", json={"confirm": True}, timeout=60)
            resp.raise_for_status()
            st.success("Remediation complete")
            st.json(resp.json())
        except Exception as e:
            st.error(f"Remediation failed: {e}")
