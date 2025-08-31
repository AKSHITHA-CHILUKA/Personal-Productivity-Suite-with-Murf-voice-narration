import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import os

# =====================
# Murf API Setup
# =====================
MURF_API_KEY = "ap2_c9a98db3-5e93-4438-9e12-55a57df45f0f"   # 🔑 Replace with your actual API key
MURF_URL = "https://api.murf.ai/v1/speech/text-to-speech"

headers = {
    "Authorization": f"Bearer {MURF_API_KEY}",
    "Content-Type": "application/json"
}

# =====================
# Expense Tracker Class
# =====================
class ExpenseTracker:
    def __init__(self):
        if "expenses" not in st.session_state:
            st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

    def add_expense(self, category, amount, note=""):
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Category": category,
            "Amount": float(amount),
            "Note": note
        }
        st.session_state.expenses = pd.concat(
            [st.session_state.expenses, pd.DataFrame([new_entry])],
            ignore_index=True
        )

    def get_summary(self):
        if st.session_state.expenses.empty:
            return "No expenses recorded yet."
        summary = st.session_state.expenses.groupby("Category")["Amount"].sum().to_dict()
        total = st.session_state.expenses["Amount"].sum()
        summary_text = "Here is your expense summary:\n"
        for cat, amt in summary.items():
            summary_text += f"- {cat}: ${amt:.2f}\n"
        summary_text += f"Total spent: ${total:.2f}"
        return summary_text

# =====================
# Murf API - Text to Speech
# =====================
def text_to_speech_murf(text, voice="en-US-Wavenet-D", output_file="summary.mp3"):
    payload = {
        "voiceId": voice,   # Choose voice from Murf API docs
        "text": text,
        "format": "MP3",
        "sampleRate": "44100"
    }
    response = requests.post(MURF_URL, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        return output_file
    else:
        st.error(f"❌ Error from Murf API: {response.text}")
        return None

# =====================
# Streamlit UI
# =====================
def main():
    st.title("💸 Voice-Enabled Expense Tracker")
    st.write("Track your expenses and get a voice summary using **Murf API** 🎤")

    tracker = ExpenseTracker()

    # --- Expense Input Form ---
    with st.form("expense_form"):
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        note = st.text_input("Note (optional)")
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            tracker.add_expense(category, amount, note)
            st.success(f"✅ Added {category} - ${amount:.2f}")

    # --- Display Expenses ---
    if not st.session_state.expenses.empty:
        st.subheader("📊 Expense Records")
        st.dataframe(st.session_state.expenses, use_container_width=True)

        # --- Plot Pie Chart ---
        st.subheader("📈 Expense Distribution")
        fig, ax = plt.subplots()
        category_totals = st.session_state.expenses.groupby("Category")["Amount"].sum()
        ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        # --- Summary ---
        summary = tracker.get_summary()
        st.subheader("📝 Expense Summary")
        st.text(summary)

        # --- Generate Voice Summary ---
        if st.button("🔊 Generate Voice Summary"):
            output_file = text_to_speech_murf(summary, voice="en-US-male", output_file="expense_summary.mp3")
            if output_file and os.path.exists(output_file):
                st.audio(output_file, format="audio/mp3")

if __name__ == "__main__":
    main()
