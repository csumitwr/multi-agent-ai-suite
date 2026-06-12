import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

def load_css():
    with open(
        "frontend/styles.css",
        encoding="utf-8"
    ) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.set_page_config(
    page_title="Multi-Agent AI Python Code Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()

st.markdown("""
# Multi-Agent AI Python Code Generator
""")

st.markdown(
    """
    **Agent 1 (Code Generator):** Qwen2.5-Coder-1.5B | **Agent 2 (Code Reviewer):** Qwen2.5-Coder-3B
    """
)

DEFAULTS = {
    "generated_code": "",
    "stdout": "",
    "stderr": "",
    "success": False,
    "attempts": 0
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

try:
    response = requests.get(
        f"{API_URL}/status",
        timeout=3
    )
    response.raise_for_status()
    status = response.json()

except:
    status = {
        "model_name": "Unavailable",
        "runtime": "Unknown"
    }
    st.error(
        "Backend not running."
    )


prompt = st.text_area(
    " ",
    height=220,
    placeholder="Generate any Python code..."
)

b1, b2, _ = st.columns(
    [1, 1, 8]
)
with b1:
    generate = st.button(
        "Generate",
        use_container_width=True
    )
with b2:
    reset = st.button(
        "Reset",
        use_container_width=True
    )

if generate:
    if not prompt.strip():
        st.warning(
            "Please enter a prompt."
        )

    else:
        with st.spinner(
            "Generating..."
        ):
            try:
                response = requests.post(
                    f"{API_URL}/generate",
                    json={
                        "prompt": prompt
                    },
                    timeout=300
                )

                if response.status_code == 200:
                    result = response.json()

                    st.session_state.generated_code = result["code"]
                    st.session_state.stdout = result["stdout"]
                    st.session_state.stderr = result["stderr"]
                    st.session_state.success = result["success"]
                    st.session_state.attempts = result["attempts"]

                else:
                    st.error(
                        response.text
                    )

            except Exception as e:
                st.error(
                    str(e)
                )

if reset:
    try:
        response = requests.post(
            f"{API_URL}/reset"
        )

        if response.status_code == 200:
            for k, v in DEFAULTS.items():
                st.session_state[k] = v

            st.rerun()

    except Exception as e:
        st.error(
            str(e)
        )

st.divider()

st.subheader(
    "Generated Python Code"
)
st.code(
    st.session_state.generated_code,
    language="python"
)
st.divider()

m1, m2, _ = st.columns(
    [1.5, 1.5, 5]
)
with m1:
    st.metric(
        "Success",
        str(
            st.session_state.success
        )
    )

with m2:
    st.metric(
        "Attempts",
        st.session_state.attempts
    )

st.divider()

with st.expander(
    "STDOUT",
    expanded=True
):
    st.code(
        st.session_state.stdout
    )

with st.expander(
    "STDERR",
    expanded=False
):
    st.code(
        st.session_state.stderr
    )