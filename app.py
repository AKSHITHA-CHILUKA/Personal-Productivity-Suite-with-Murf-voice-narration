import os
import streamlit as st
from murf import Murf
import pandas as pd
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
MURF_API_KEY="ap2_c9a98db3-5e93-4438-9e12-55a57df45f0f" # Set in .env or replace here

# Initialize Murf client
client = Murf(api_key=MURF_API_KEY)

# ---------------------------
# MURF FUNCTIONS
# ---------------------------
def generate_voice_summary(text, voice_id="en-US-natalie"):
    """Generate voice from text using Murf SDK."""
    try:
        response = client.text_to_speech.generate(
            text=text,
            voice_id=voice_id
        )
        audio_url = response.audio_file
        return audio_url, None

    except Exception as e:
        return None, f"⚠️ Exception: {e}"

# ---------------------------
# UI Styling
# ---------------------------
def local_css():
    st.markdown("""
    <style>
    .metric-card {
        background-color: #2a2a39;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: white;
        border: 1px solid #4f4f6a;
    }
    .metric-card h3 {
        font-size: 18px;
        color: #a9a9b3;
    }
    .metric-card p {
        font-size: 28px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="Voice-Enabled Expense Tracker", layout="wide", page_icon="💰")
local_css()

st.title("💰 Professional Expense Dashboard")
st.markdown("Add your expenses in the sidebar and see your financial dashboard updated in real-time.")

# Store data in session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("📝 Add an Expense")
    with st.form("expense_form", clear_on_submit=True):
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
            st.rerun()
    
    st.divider()
    if st.session_state["expenses"]:
        if st.button("🗑️ Clear All Expenses"):
            st.session_state["expenses"] = []
            st.rerun()
    
    st.divider()
    st.header("🕒 Recent Activity")
    if st.session_state["expenses"]:
        for expense in st.session_state["expenses"][-5:]:
            st.write(f"• {expense['category']}: ₹{expense['amount']:.2f}")
    else:
        st.write("No recent activity.")


# --- Main Page for Dashboard ---
if st.session_state["expenses"]:
    df = pd.DataFrame(st.session_state["expenses"])
    df['date'] = pd.to_datetime(df['date'])

    # --- Key Metrics ---
    total_spent = df["amount"].sum()
    avg_daily_spend = df.groupby(df['date'].dt.date)['amount'].sum().mean()
    highest_expense = df['amount'].max()

    st.header("Dashboard Overview", divider='rainbow')
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><h3>Total Spent</h3><p>₹{total_spent:,.2f}</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><h3>Average Daily Spend</h3><p>₹{avg_daily_spend:,.2f}</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><h3>Highest Expense</h3><p>₹{highest_expense:,.2f}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Create tabs
    tab1, tab2 = st.tabs(["📊 Visual Dashboard", "📜 Raw Data"])

    with tab1:
        st.subheader("Spending Analysis")
        
        # Prepare data for charts
        by_category = df.groupby("category")["amount"].sum()
        df_time = df.set_index('date').resample('D')['amount'].sum()

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("By Category")
            st.bar_chart(by_category)

        with col2:
            st.subheader("Over Time")
            st.area_chart(df_time)

        st.divider()

        # Voice Summary
        st.subheader("🔊 Generate Voice Summary")
        summary_text = f"You have spent a total of {total_spent:,.2f} rupees. Your average daily spending is {avg_daily_spend:,.2f} rupees. "
        by_category = df.groupby("category")["amount"].sum()
        for category, amount in by_category.items():
            summary_text += f"On {category}, you spent {amount:,.2f} rupees. "

        if st.button("🎤 Generate & Play Summary"):
            with st.spinner("Generating voice summary..."):
                audio_url, error = generate_voice_summary(summary_text)
                if error:
                    st.error(error)
                else:
                    st.audio(audio_url, autoplay=True)
    
    with tab2:
        st.subheader("All Expenses")
        st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name='expenses.csv',
            mime='text/csv',
        )

else:
    st.info("ℹ️ Add an expense using the form in the sidebar to build your dashboard.")
