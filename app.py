import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

os.environ["GOOGLE_API_KEY"] = os.getenv("gemini_key")

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🎯",
    layout="centered"
)

# -------------------------------------------------
# Custom Professional Styling
# -------------------------------------------------
st.markdown("""
<style>

/* Global Background */
.stApp {
    background: linear-gradient(to right, #eef2ff, #f8fafc);
    font-family: 'Poppins', sans-serif;
    color: #1e293b;
}

header {visibility: hidden;}

.main > div {
    max-width: 900px;
    margin: auto;
    padding-bottom: 110px;
}

/* Title */
h1 {
    text-align: center;
    color: #1d4ed8;
}

/* Chat Bubbles */
.user-bubble {
    background: #dbeafe;
    padding: 14px 20px;
    border-radius: 18px;
    margin: 10px 0;
    max-width: 75%;
    margin-left: auto;
    color: #1e3a8a;
}

.bot-bubble {
    background: #f1f5f9;
    padding: 14px 20px;
    border-radius: 18px;
    margin: 10px 0;
    max-width: 75%;
    color: #0f172a;
}

/* Fixed Input */
div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 15px 20px;
    border-top: 1px solid #cbd5e1;
    z-index: 999;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #dbeafe, #ffffff);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar Controls
# -------------------------------------------------
st.sidebar.title("⚙️ Career Settings")

temperature = st.sidebar.slider(
    "Creativity (Temperature)",
    0.0, 1.0, 0.5, 0.1
)

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    st.rerun()

# -------------------------------------------------
# System Prompt (Advanced Prompt Engineering)
# -------------------------------------------------
system_prompt = """
You are an AI Career Advisor and Skill Strategy Consultant.

Goal: Provide structured, practical, and personalized career guidance.

First, extract:
Education | Current Skills | Target Role | Experience Level | Industry | Location

Output Format (STRICTLY structured and concise):

1. Career Insight (clear direction in 3–4 bullets)
2. Skill Gap Analysis (missing skills in bullets)
3. Learning Roadmap (step-by-step practical plan)
4. Recommended Resources (max 5)
5. Resume Improvement Tips (3 bullets)
6. Interview Preparation Focus (3 bullets)
7. Market Demand Insight (short realistic note)
8. Motivation Boost (1 short line)

Rules:
- No generic advice.
- No long paragraphs.
- No storytelling.
- Max 400 words total.
- Use bullets only.
- Be practical and actionable.
"""

# -------------------------------------------------
# Initialize Gemini Client
# -------------------------------------------------
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

client = st.session_state.client

# -------------------------------------------------
# Initialize Chat Session
# -------------------------------------------------
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature
        )
    )

# -------------------------------------------------
# Store Conversation History
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("<h1>🎯 AI Career Advisor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#475569;'>Personalized Career Guidance Powered by Gemini</p>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# Display Chat Messages
# -------------------------------------------------
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user-bubble'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{text}</div>", unsafe_allow_html=True)

# -------------------------------------------------
# Chat Input
# -------------------------------------------------
user_input = st.chat_input("Ask about your career...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    chat = st.session_state.chat_session

    with st.spinner("Analyzing your career profile..."):
        response = chat.send_message(user_input)

    bot_reply = response.text
    st.session_state.messages.append(("bot", bot_reply))

    st.rerun()