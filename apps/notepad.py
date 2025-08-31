import streamlit as st
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
    st.title("📝 Simple Notepad")
    st.markdown("Jot down your thoughts, ideas, or reminders. Your notes are saved automatically.")

    # Initialize session state for note content
    if 'note_content' not in st.session_state:
        st.session_state.note_content = ""

    # --- Text Area for Notes ---
    st.session_state.note_content = st.text_area(
        "Your Notes",
        value=st.session_state.note_content,
        height=400,
        label_visibility="collapsed"
    )

    st.divider()

    # --- Action Buttons ---
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Clear Note", use_container_width=True):
            st.session_state.note_content = ""
            st.rerun()
    with col2:
        st.download_button(
            label="📥 Download Note as TXT",
            data=st.session_state.note_content,
            file_name="my_note.txt",
            mime="text/plain",
            use_container_width=True,
            disabled=not st.session_state.note_content
        )
    with col3:
        if st.button("🎤 Read My Note", use_container_width=True, disabled=not st.session_state.note_content):
            with st.spinner("Generating audio..."):
                audio_url, error = generate_voice(st.session_state.note_content)
                if error:
                    st.error(error)
                else:
                    st.audio(audio_url, autoplay=True)
