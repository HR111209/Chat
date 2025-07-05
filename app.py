import streamlit as st
from datetime import datetime
import os
import time

# Constants
PASSWORD = "1234"
CHAT_LOG_FILE = "chat_log.txt"
REFRESH_INTERVAL = 5  # seconds

# User-specific styles
USER_STYLES = {
    "Harshit": {"bg_color": "#e0f0ff", "text_color": "#1f77b4"},
    "Friend": {"bg_color": "#d4f9d4", "text_color": "#2ca02c"},
}

# Init session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

# Read/write helpers
def read_chat_log():
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as file:
            return file.readlines()
    return []

def write_to_chat_log(message):
    with open(CHAT_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(message + "\n")

# Login screen
def login():
    st.title("🔒 Secure Chat Login")
    username = st.text_input("Enter your name (e.g., Rohit):")
    password = st.text_input("Enter password:", type="password")

    if st.button("Login"):
        if password == PASSWORD and username.strip() != "":
            st.session_state.authenticated = True
            st.session_state.username = username.strip()
            join_msg = f"SYSMSG: {username} joined at {datetime.now().strftime('%b %d, %Y %I:%M %p')}"
            write_to_chat_log(join_msg)
            st.rerun()
        else:
            st.error("❌ Incorrect credentials")

# Render chat message as bubble
def render_chat_bubble(user, message, timestamp):
    style = USER_STYLES.get(user, {"bg_color": "#f0f0f0", "text_color": "#000"})
    return f"""
    <div style='background-color:{style["bg_color"]}; color:{style["text_color"]}; 
                padding:8px; border-radius:12px; margin:6px 0; width:fit-content;
                max-width:90%; word-wrap:break-word; font-size:16px;'>
        <b>{user}</b> <span style='font-size:11px; color:gray;'>({timestamp})</span><br>
        {message}
    </div>
    """

# Send message logic
def submit_message():
    user_input = st.session_state.chat_input.strip()
    if user_input:
        timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
        msg = f"[{timestamp}] {st.session_state.username}: {user_input}"
        write_to_chat_log(msg)
        st.session_state.chat_input = ""
        st.rerun()

# Chat interface
def chat():
    st.markdown("<h3 style='margin-bottom: 0;'>💬 Private Chat Room</h3>", unsafe_allow_html=True)

    chat_log = read_chat_log()
    system_msgs = []
    chat_msgs = []

    for line in chat_log:
        if line.startswith("SYSMSG:"):
            system_msgs.append(line.replace("SYSMSG:", "").strip())
        else:
            chat_msgs.append(line.strip())

    # System notifications (top-left)
    with st.container():
        for msg in system_msgs[-3:]:
            st.markdown(f"<div style='text-align:left; color:gray; font-size:13px;'>🔔 {msg}</div>", unsafe_allow_html=True)

    # Chat messages
    with st.container():
        st.markdown("<div style='max-height: 55vh; overflow-y: auto; border: 1px solid #ccc; border-radius: 10px; padding: 10px;'>", unsafe_allow_html=True)
        for line in chat_msgs:
            try:
                timestamp = line.split("]")[0].replace("[", "")
                user = line.split("]")[1].split(":")[0].strip()
                msg = ":".join(line.split(":")[1:]).strip()
                st.markdown(render_chat_bubble(user, msg, timestamp), unsafe_allow_html=True)
            except:
                st.write(line)
        st.markdown("</div>", unsafe_allow_html=True)

    # Chat input (fixed at bottom)
    with st.container():
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.text_input(
            "Type your message (emoji supported 😊):",
            key="chat_input",
            label_visibility="collapsed",
            on_change=submit_message
        )
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            pass
        with col2:
            if st.button("Send"):
                submit_message()

    # Footer + Logout
    st.markdown(f"<div style='color:gray; font-size:12px;'>🔁 Refreshing every {REFRESH_INTERVAL}s</div>", unsafe_allow_html=True)
    if st.button("Logout"):
        leave_msg = f"SYSMSG: {st.session_state.username} left at {datetime.now().strftime('%b %d, %Y %I:%M %p')}"
        write_to_chat_log(leave_msg)
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    # Auto-refresh
    time.sleep(REFRESH_INTERVAL)
    st.rerun()

# App runner
if st.session_state.authenticated:
    chat()
else:
    login()
