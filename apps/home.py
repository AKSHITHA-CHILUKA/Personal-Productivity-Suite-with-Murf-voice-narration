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
    st.title("🚀 Personal Productivity Suite")
    st.markdown("---")

    if st.button("🎤 Play Welcome Message"):
        welcome_text = "Welcome to your personal productivity suite! Select an application from the sidebar to get started."
        with st.spinner("Generating welcome message..."):
            audio_url, error = generate_voice(welcome_text)
            if error:
                st.error(error)
            else:
                st.audio(audio_url, autoplay=True)

    st.subheader("Welcome to your all-in-one personal dashboard!")
    st.markdown("""
    This application is a collection of tools to help you manage different aspects of your daily life. 
    Use the navigation menu on the left to switch between the different apps.
    """)

    st.header("Available Apps")
    
    # Build the list of apps as a list of strings
    app_list = [
        "- **💰 Expense Tracker**: A powerful tool to monitor your spending, set budgets, and get voice-narrated summaries of your financial activity.",
        "- **✅ To-Do List**: A simple yet effective task manager to keep track of your daily tasks.",
        "- **⚖️ BMI Calculator**: A health utility to quickly calculate and assess your Body Mass Index.",
        "- **🍅 Pomodoro Timer**: A productivity timer to help you focus using the Pomodoro Technique.",
        "- **📝 Simple Notepad**: A digital scratchpad for your thoughts and ideas.",
        "- **🔐 Password Generator**: Create strong, random passwords to enhance your security.",
        "- **📈 Simple Interest Calculator**: A handy tool for calculating simple interest on loans or investments."
    ]
    
    # Render the entire list in a single markdown block
    st.markdown("\n".join(app_list))

    st.markdown("\nSelect an app from the sidebar to get started!")
