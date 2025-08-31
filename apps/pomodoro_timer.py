import streamlit as st
import time
from murf import Murf

# --- Murf AI Setup ---
MURF_API_KEY="ap2_c9a98db3-5e93-4438-9e12-55a57df45f0f"
client = Murf(api_key=MURF_API_KEY)

def generate_voice(text):
    try:
        response = client.text_to_speech.generate(text=text, voice_id="en-US-natalie")
        return response.audio_file, None
    except Exception as e:
        return None, f"⚠️ Exception: {e}"

def run():
    st.title("🍅 Pomodoro Timer")
    st.markdown("Stay focused and productive with the Pomodoro Technique.")

    # Initialize session state variables
    if 'pomodoro_mode' not in st.session_state:
        st.session_state.pomodoro_mode = 'Work'  # 'Work', 'Short Break', 'Long Break'
    if 'pomodoro_time_left' not in st.session_state:
        st.session_state.pomodoro_time_left = 25 * 60  # 25 minutes
    if 'pomodoro_running' not in st.session_state:
        st.session_state.pomodoro_running = False

    # Timer settings
    work_duration = 25 * 60
    short_break_duration = 5 * 60
    long_break_duration = 15 * 60

    # --- Timer Display ---
    mode_text = f"Current Mode: **{st.session_state.pomodoro_mode}**"
    st.markdown(f"### {mode_text}")
    
    minutes, seconds = divmod(st.session_state.pomodoro_time_left, 60)
    timer_display = st.empty()
    timer_display.markdown(f"<h1 style='text-align: center; font-size: 6em;'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)

    # --- Controls ---
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Start", use_container_width=True, disabled=st.session_state.pomodoro_running):
            st.session_state.pomodoro_running = True
            st.rerun()
    with col2:
        if st.button("⏸️ Pause", use_container_width=True, disabled=not st.session_state.pomodoro_running):
            st.session_state.pomodoro_running = False
            st.rerun()
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.pomodoro_running = False
            if st.session_state.pomodoro_mode == 'Work':
                st.session_state.pomodoro_time_left = work_duration
            else:
                st.session_state.pomodoro_time_left = short_break_duration
            st.rerun()

    # --- Timer Logic ---
    if st.session_state.pomodoro_running:
        while st.session_state.pomodoro_time_left > 0:
            st.session_state.pomodoro_time_left -= 1
            time.sleep(1)
            minutes, seconds = divmod(st.session_state.pomodoro_time_left, 60)
            timer_display.markdown(f"<h1 style='text-align: center; font-size: 6em;'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)
        
        st.session_state.pomodoro_running = False
        st.balloons()
        
        notification_text = ""
        # Switch modes
        if st.session_state.pomodoro_mode == 'Work':
            notification_text = "Work session complete. Time for a short break."
            st.session_state.pomodoro_mode = 'Short Break'
            st.session_state.pomodoro_time_left = short_break_duration
        else: # If it was a break
            notification_text = "Break is over. Time to get back to work."
            st.session_state.pomodoro_mode = 'Work'
            st.session_state.pomodoro_time_left = work_duration
        
        # Play voice notification
        with st.spinner("Generating notification..."):
            audio_url, error = generate_voice(notification_text)
            if not error:
                st.audio(audio_url, autoplay=True)

        st.rerun()
