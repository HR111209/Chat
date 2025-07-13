import streamlit as st
from datetime import datetime
import os
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --------------------- CONFIG ---------------------
st.set_page_config(page_title="NEET UG 2025 Portal", layout="centered", initial_sidebar_state="collapsed")
PASSWORD = "111209"
CHAT_LOG_FILE = "chat_log.txt"
REFRESH_INTERVAL = 5  # in seconds

# --------------------- SESSION STATE ---------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

# --------------------- CHAT HELPERS ---------------------
def read_chat_log():
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as file:
            return file.readlines()
    return []

def write_to_chat_log(message):
    with open(CHAT_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(message + "\n")

def submit_message():
    user_input = st.session_state.chat_input.strip()
    if user_input:
        timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
        msg = f"[{timestamp}] {st.session_state.username}: {user_input}"
        write_to_chat_log(msg)
        st.session_state.chat_input = ""

def render_chat_bubble(user, message, timestamp):
    color = "#d9fdd3" if user == st.session_state.username else "#f0f0f0"
    return f"""
    <div style='background-color:{color}; padding:10px; border-radius:10px; margin:6px 0; max-width:80%; word-wrap:break-word;'>
        <b>{user}</b> <span style='font-size:11px; color:gray;'>({timestamp})</span><br>
        {message}
    </div>
    """

# --------------------- MAP ---------------------
def show_college_map():
    st.subheader("🗺️ Explore Top Medical Colleges on Map")

    data = pd.DataFrame([
        {"College": "AIIMS Delhi", "City": "New Delhi", "Lat": 28.5672, "Lon": 77.2100, "State": "Delhi", "Rank": 1},
        {"College": "JIPMER", "City": "Puducherry", "Lat": 11.9416, "Lon": 79.8083, "State": "Puducherry", "Rank": 2},
        {"College": "MAMC", "City": "New Delhi", "Lat": 28.6353, "Lon": 77.2249, "State": "Delhi", "Rank": 3},
        {"College": "KGMU", "City": "Lucknow", "Lat": 26.8705, "Lon": 80.9462, "State": "Uttar Pradesh", "Rank": 4},
        {"College": "BHU IMS", "City": "Varanasi", "Lat": 25.2677, "Lon": 82.9913, "State": "Uttar Pradesh", "Rank": 5},
        {"College": "Grant Medical College", "City": "Mumbai", "Lat": 18.9543, "Lon": 72.8295, "State": "Maharashtra", "Rank": 6},
        {"College": "Seth GS Medical College", "City": "Mumbai", "Lat": 19.0165, "Lon": 72.8436, "State": "Maharashtra", "Rank": 7},
        {"College": "Stanley Medical College", "City": "Chennai", "Lat": 13.1007, "Lon": 80.2936, "State": "Tamil Nadu", "Rank": 8},
        {"College": "VMMC", "City": "New Delhi", "Lat": 28.5830, "Lon": 77.1859, "State": "Delhi", "Rank": 9},
        {"College": "GMC Chandigarh", "City": "Chandigarh", "Lat": 30.7333, "Lon": 76.7794, "State": "Chandigarh", "Rank": 10},
        {"College": "Lady Hardinge Medical College", "City": "Delhi", "Lat": 28.6315, "Lon": 77.2157, "State": "Delhi", "Rank": 11},
    ])

    data = data.rename(columns={"Lat": "lat", "Lon": "lon"})

    st.map(data[["lat", "lon"]], zoom=4, use_container_width=True)

    with st.expander("📋 View College Data Table"):
        st.dataframe(data[["Rank", "College", "City", "State"]], use_container_width=True)

# --------------------- NEET PORTAL ---------------------
def show_neet_info():
    st.title("🧪 NEET UG 2025 Portal")
    st.markdown("Welcome to the NEET UG 2025 Information Portal. Find all syllabus, eligibility, cutoff, and exam-related info below.")

    with st.expander("📚 NEET Syllabus - Physics"):
        st.markdown("**Class 11:** Kinematics, Laws of Motion, Gravitation, Thermodynamics, Oscillations, Waves")
        st.markdown("**Class 12:** Electrostatics, Current Electricity, Magnetic Effects, Optics, Atoms, Nuclei")

    with st.expander("🧪 NEET Syllabus - Chemistry"):
        st.markdown("**Class 11:** Mole Concepts, Atomic Structure, Bonding, Thermodynamics, Hydrocarbons")
        st.markdown("**Class 12:** Solid State, Electrochemistry, Surface Chemistry, Organic Compounds, Biomolecules")

    with st.expander("🌿 NEET Syllabus - Biology"):
        st.markdown("**Class 11:** Diversity, Cell Structure, Plant Physiology, Human Physiology")
        st.markdown("**Class 12:** Reproduction, Genetics, Evolution, Human Health, Biotechnology")

    with st.expander("📊 Exam Pattern & Marking Scheme"):
        st.markdown("""
        | Subject     | Questions (to attempt) | Marks |
        |-------------|------------------------|-------|
        | Physics     | 45 out of 50           | 180   |
        | Chemistry   | 45 out of 50           | 180   |
        | Biology     | 90 out of 100          | 360   |
        | **Total**   | 180 out of 200         | 720   |

        **Marking**: +4 for correct | -1 for wrong | 0 for unattempted
        """)

    with st.expander("✅ Eligibility Criteria"):
        st.markdown("""
        - Minimum age: 17 years as on 31st December of admission year  
        - Academic qualification: 10+2 with Physics, Chemistry, Biology/Biotechnology and English  
        - Qualifying marks: Minimum 50% for UR, 40% for SC/ST/OBC  
        - Attempts: Unlimited  
        - Nationality: Indian, NRI, OCI, PIO, or Foreign Nationals
        """)

    with st.expander("🏫 Top Government Medical Colleges (India)"):
        st.markdown("""
        1. AIIMS Delhi  
        2. JIPMER Puducherry  
        3. Maulana Azad Medical College (MAMC), Delhi  
        4. Grant Medical College, Mumbai  
        5. BHU Varanasi  
        6. KGMU Lucknow  
        7. Stanley Medical College, Chennai  
        8. Seth GS Medical College, Mumbai  
        9. Institute of Medical Sciences, BHU  
        10. Lady Hardinge Medical College, Delhi
        """)

    with st.expander("📉 NEET Previous Year AIQ Cutoff (General Category)"):
        st.markdown("""
        | College                        | Closing Rank 2023 |
        |-------------------------------|--------------------|
        | AIIMS Delhi                   | 57                 |
        | Maulana Azad Medical College  | 90                 |
        | BHU Varanasi                  | 850                |
        | VMMC Delhi                    | 110                |
        | KGMU Lucknow                  | 1300               |
        | JIPMER Puducherry             | 300                |
        | Stanley Medical College       | 2700               |
        | GMC Chandigarh                | 800                |
        """)

    with st.expander("📝 Preparation Tips & Strategy"):
        st.markdown("""
        - Understand the syllabus thoroughly (NCERT is key).
        - Mock tests and previous year papers are critical.
        - Time management: Solve MCQs with speed and accuracy.
        - Make a realistic timetable and stick to it.
        - Focus on weak topics every week.
        - Use apps or tools like NEETprep, Unacademy, Embibe, etc.
        """)

    show_college_map()

    st.markdown("---")
    if st.button("🔐 Admin Panel"):
        st.session_state.show_login = True

# --------------------- LOGIN ---------------------
def login_panel():
    st.subheader("🔐 Admin Login")
    username = st.text_input("Enter your name:")
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

# --------------------- CHAT ---------------------
def chat_panel():
    st.subheader("💬 Admin Chat")
    st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="chat_refresh")

    chat_log = read_chat_log()
    for line in chat_log[-50:]:
        if line.startswith("SYSMSG:"):
            st.markdown(f"<div style='color:gray; font-size:12px;'>🔔 {line[7:]}</div>", unsafe_allow_html=True)
        else:
            try:
                timestamp = line.split("]")[0].replace("[", "")
                user = line.split("]")[1].split(":")[0].strip()
                msg = ":".join(line.split(":")[1:]).strip()
                st.markdown(render_chat_bubble(user, msg, timestamp), unsafe_allow_html=True)
            except:
                st.markdown(line)

    st.text_input("Type your message here...", key="chat_input", label_visibility="collapsed", on_change=submit_message)
    if st.button("Send"):
        submit_message()

    if st.button("Logout"):
        leave_msg = f"SYSMSG: {st.session_state.username} left at {datetime.now().strftime('%b %d, %Y %I:%M %p')}"
        write_to_chat_log(leave_msg)
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

# --------------------- MAIN ---------------------
def main():
    if st.session_state.authenticated:
        chat_panel()
    elif "show_login" in st.session_state and st.session_state.show_login:
        login_panel()
    else:
        show_neet_info()

main()
