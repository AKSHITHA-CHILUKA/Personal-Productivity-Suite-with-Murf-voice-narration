import os
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
MURF_API_KEY="ap2_c9a98db3-5e93-4438-9e12-55a57df45f0f"

# Set in .env or replace here
MURF_BASE_URL = "https://api.murf.ai/v1"

headers = {
    "Authorization": f"Bearer {MURF_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------------------
# MURF FUNCTIONS
# ---------------------------
def generate_voice_summary(text, voice_id="en-US_natalie_-_neural"):
    """Generate voice from text using Murf API."""
    try:
        # Use the direct text-to-speech synthesis endpoint
        tts_url = f"{MURF_BASE_URL}/speech/text-to-speech"
        
        payload = {
            "text": text,
            "voiceId": voice_id,
            "format": "MP3",
            "sampleRate": 44100
        }

        response = requests.post(tts_url, headers=headers, json=payload)

        if response.status_code != 200:
            return None, f"❌ Failed to generate speech: {response.text}"

        # The response contains the audio content directly
        # To play it in streamlit, we need to save it to a file or serve it
        # For simplicity, we can return the content and let the UI handle it.
        # However, st.audio needs a URL or a file path. Let's get the URL from the response if available.
        # Based on Murf documentation, the direct TTS API returns an audio file URL.
        
        audio_url = response.json().get("audioFileUrl")
        if not audio_url:
             # If the direct audio URL is not in the response, let's check for the content
             # And save it to a file as a fallback.
            if response.content:
                with open("summary.mp3", "wb") as f:
                    f.write(response.content)
                return "summary.mp3", None
            return None, "❌ No audio URL or content returned."

        return audio_url, None

    except Exception as e:
        return None, f"⚠️ Exception: {e}"


# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="Expense Tracker with Murf AI", layout="centered")
st.title("💰 Personal Expense Tracker + Murf AI Voice Summary")

# Store data in session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# Add expense form
with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
    amount = st.number_input("Amount", min_value=1.0, step=0.5)
    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        st.session_state["expenses"].append({
            "date": str(date),
            "category": category,
            "amount": amount
        })
        st.success("✅ Expense added!")

# Display expense table
if st.session_state["expenses"]:
    df = pd.DataFrame(st.session_state["expenses"])
    st.subheader("📊 Expense History")
    st.dataframe(df)

    # Summary
    total = df["amount"].sum()
    by_category = df.groupby("category")["amount"].sum().reset_index()

    st.metric("Total Spent", f"₹{total:.2f}")
    st.bar_chart(by_category.set_index("category"))

    # Voice Summary
    st.subheader("🔊 Generate Voice Summary")
    summary_text = f"You have spent a total of {total:.2f} rupees. "
    for _, row in by_category.iterrows():
        summary_text += f"On {row['category']}, you spent {row['amount']:.2f} rupees. "

    if st.button("🎤 Generate Voice"):
        with st.spinner("Generating voice summary..."):
            audio_url, error = generate_voice_summary(summary_text)
            if error:
                st.error(error)
            else:
                st.audio(audio_url)
else:
    st.info("ℹ️ Add some expenses to see the summary.")
