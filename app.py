import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment file
load_dotenv()

# Try to import Gemini SDK
USE_GEMINI = True
try:
    import google.generativeai as genai
except:
    USE_GEMINI = False

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Bunny Chat 🐰", page_icon="🐰", layout="wide")

# ------------------ STYLES + FLOATING EMOJIS ------------------
st.markdown("""
<style>
/* Text input label */
label {
    color: #000000 !important;
    font-weight: 600;
}

.stApp {
    background: linear-gradient(120deg, #FFF7FB, #FFE6F5, #F9FFFB);
    overflow: hidden;
    font-family: 'Poppins', sans-serif;
}

/* Floating Emoji FIXED */
.floating-emoji {
    position: fixed;
    z-index: 0 !important;
    opacity: 0.22 !important;
    font-size: 60px;
    pointer-events: none;
    animation: float 8s infinite ease-in-out;
}

.e1 { top: 10%; left: 8%; animation-duration: 12s; }
.e2 { top: 20%; right: 10%; animation-duration: 10s; }
.e3 { bottom: 15%; left: 42%; animation-duration: 14s; }
.e4 { bottom: 25%; right: 25%; animation-duration: 11s; }

@keyframes float {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-25px) rotate(6deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

/* Chat bubbles */
.chat-bubble {
    padding: 12px 15px;
    border-radius: 14px;
    max-width: 70%;
    white-space: pre-wrap;
    line-height: 1.4;
    margin-bottom: 6px;
}

.user-bubble {
    background: #ffe4f2;
    border: 1px solid #ffb8d9;
    color: #5a0034;
    margin-left: auto;
    border-bottom-right-radius: 5px;
}

.bot-bubble {
    background: white;
    border: 1px solid #ffd3ea;
    color: #000000;
    margin-right: auto;
    border-bottom-left-radius: 5px;
}

/* Avatars */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 22px;
}

/* Message rows */
.row-user {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
}
.row-bot {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
}

.timestamp {
    font-size: 11px;
    color: #9c6f8a;
    margin-top: 2px;
}

.center-text {
    text-align:center;
    color:#d94f9b;
    font-weight:600;
}

</style>

<!-- Floating Emojis -->
<div class="floating-emoji e1">🌸</div>
<div class="floating-emoji e2">💖</div>
<div class="floating-emoji e3">✨</div>
<div class="floating-emoji e4">🐰</div>

""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.title("✨ Options")

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
        st.success("Chat cleared!")

    # Download chat
    def txt_chat():
        return "\n".join([f"[{m['time']}] {m['role']} : {m['text']}" for m in st.session_state.history])

    st.download_button("⬇️ Download .txt", txt_chat(), "chat.txt")

    st.download_button("⬇️ Download .json",
                       json.dumps(st.session_state.history, indent=2),
                       "chat.json")

# ------------------ TITLE ------------------
st.markdown("<h1 style='text-align:center; color:#000000;'>🐰 Bunny Chat</h1>", unsafe_allow_html=True)
st.markdown("<p class='center-text' style='font-size:14px;'>Your cute aesthetic AI friend 💖</p>", unsafe_allow_html=True)

# ------------------ CHAT HISTORY ------------------
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="row-user">
                <div class="chat-bubble user-bubble">{msg['text']}</div>
                <div class="avatar">😊</div>
            </div>
            <div class="timestamp" style="text-align:right;">{msg['time']}</div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="row-bot">
                <div class="avatar">🐰</div>
                <div class="chat-bubble bot-bubble">{msg['text']}</div>
            </div>
            <div class="timestamp">{msg['time']}</div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ------------------ USER INPUT ------------------
user_input = st.text_input("Type your message here:")

if st.button("Send") and user_input.strip():

    now = datetime.now().strftime("%H:%M")
    st.session_state.history.append({
        "role": "user",
        "text": user_input,
        "time": now
    })

    # Gemini API call
    KEY = os.getenv("GEMINI_API_KEY")

    if KEY and USE_GEMINI:
        try:
            genai.configure(api_key=KEY)
            model = genai.GenerativeModel("gemini-2.0-flash")

            sys_prompt = "You are a cute bunny assistant. Keep replies sweet, short, and aesthetic. Add emojis."
            prompt = f"{sys_prompt}\nUser: {user_input}\nAssistant:"

            response = model.generate_content(prompt)

            try:
                bot_reply = response.candidates[0].content.parts[0].text
            except:
                bot_reply = response.text

        except Exception as e:
            bot_reply = f"AI Error: {e}"

    else:
        bot_reply = "Your Gemini API key is missing 💔 Add it in `.env` as:\n\nGEMINI_API_KEY=yourkey"

    now2 = datetime.now().strftime("%H:%M")
    st.session_state.history.append({
        "role": "bot",
        "text": bot_reply,
        "time": now2
    })

    st.rerun()


st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;

    transform: translateX(-60px);   /* ⭐ shift left ~1 inch */
    
    padding: 8px 0;
    font-size: 14px;
    color: #d94f9b;
    opacity: 0.9;
    z-index: 9999;
}
</style>

<div class="footer">Made with 💖 by Safakhanum</div>
""", unsafe_allow_html=True)
