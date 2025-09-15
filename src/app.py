import os
import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import html

st.set_page_config(page_title="Taha's AI Chat Bot", page_icon="🤖", layout="wide")

# --- Constants ---
CSS_PATH = os.path.join(os.path.dirname(__file__), "styles.css")
ENDPOINT = "https://models.github.ai/inference"
DEFAULT_MODEL = "openai/gpt-4.1-mini"

# --- Helpers ---
def load_css(path: str) -> None:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning("styles.css not found — using inline defaults.")

def get_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if token is None:
        st.sidebar.error("GITHUB_TOKEN not set. In PowerShell run: $env:GITHUB_TOKEN='your_token' then restart Streamlit.")
        st.stop()
    return token

def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

def sidebar_controls():
    st.sidebar.markdown("## Settings")
    model = st.sidebar.selectbox("Model", [DEFAULT_MODEL], index=0)
    temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 1.0, 0.1)
    if st.sidebar.button("Clear chat"):
        st.session_state.pop("messages", None)
    return model, temperature

def render_header():
    st.markdown('<div class="card title-row"><div class="logo">Taha AI Chat Bot</div><div class="muted">Hope you have a good time</div></div>', unsafe_allow_html=True)
    st.write("")

def render_messages(container):
    with container:
        for msg in st.session_state.messages:
            role = msg.get("role", "assistant")
            content = html.escape(msg.get("content", ""))
            if role == "user":
                st.markdown(f'<div class="chat-bubble user">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble assistant">{content}</div>', unsafe_allow_html=True)

def call_model(token: str, model: str, user_input: str, temperature: float) -> str:
    client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(token))
    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage(user_input),
        ],
        temperature=float(temperature),
        top_p=1.0,
        model=model,
    )
    return response.choices[0].message.content

# --- App start ---
load_css(CSS_PATH)
token = get_token()
model, temperature = sidebar_controls()
init_session()

# Header
with st.container():
    render_header()

# Chat + controls layout
chat_col, ctrl_col = st.columns([3, 1], gap="small")
with chat_col:
    chat_box = st.container()
    render_messages(chat_box)

with ctrl_col:
    st.markdown("### Quick actions")
    st.write("Use Enter or the Send button to submit.")
    st.markdown("---")

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask the assistant...", key="user_input", placeholder="What's on your mind?")
    submitted = st.form_submit_button("Send")

if submitted:
    if not user_input:
        st.warning("Please enter a question.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        # re-render messages to show user immediately
        with chat_col:
            st.markdown(f'<div class="chat-bubble user">{html.escape(user_input)}</div>', unsafe_allow_html=True)

        try:
            with st.spinner("Thinking..."):
                assistant_text = call_model(token, model, user_input, temperature)
        except Exception as e:
            assistant_text = f"Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": assistant_text})
        with chat_col:
            st.markdown(f'<div class="chat-bubble assistant">{html.escape(assistant_text)}</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="muted" style="margin-top:18px">Built for fun</div>', unsafe_allow_html=True)