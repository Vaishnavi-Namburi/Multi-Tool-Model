import streamlit as st
from agent import agent_response
import time

st.set_page_config(
    page_title="Ray AI",
    page_icon="🤖",
    layout="wide"
)

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# Header
st.markdown("""
<div class='header'>
    <div class='main-title'>
        🤖 Ray AI
    </div>
    <div class='sub-title'>
        Weather • Stocks • Commands
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:

    st.title("🤖 Ray AI")

    st.markdown("---")

    st.markdown("""
### 🛠 Available Tools
""")

    st.markdown("""
<div class='tool-box'>
🌤 Weather Tool
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='tool-box'>
📈 Stock Market Tool
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='tool-box'>
💻 Command Tool
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    st.caption("Powered by Ollama + Qwen")


# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Input box
prompt = st.chat_input("Ask Ray anything...")


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):

        with st.spinner("🧠 Ray is thinking..."):

            time.sleep(1)

            response = agent_response(prompt)

        st.markdown(response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# Footer
st.markdown("""
<div class='footer'>
Made with ❤️ using Streamlit + Ollama + Qwen
</div>
""", unsafe_allow_html=True)