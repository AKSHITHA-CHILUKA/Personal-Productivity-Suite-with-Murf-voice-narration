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

def run():
    local_css()

    # Store data in session state
    if "expenses" not in st.session_state:
        st.session_state["expenses"] = []
    if "budget" not in st.session_state:
        st.session_state["budget"] = 0.0

    # --- Main App Flow ---
    # 1. Check if budget is set. If not, show budget entry screen.
    if st.session_state.budget == 0.0:
        st.title("Welcome! Let's Set Up Your Budget")
        st.markdown("Before you start tracking expenses, please set a monthly budget for yourself.")
        
        with st.form("budget_form"):
            new_budget = st.number_input("Enter Your Monthly Budget (₹)", min_value=1.0, step=100.0)
            submitted = st.form_submit_button("Set Budget")
            if submitted:
                st.session_state.budget = new_budget
                st.success(f"Great! Your budget is set to ₹{new_budget:,.2f}.")
                st.rerun()

    # 2. If budget is set, show the main dashboard.
    else:
        st.title("💰 Professional Expense Dashboard")
        st.markdown("Add your expenses in the sidebar and see your financial dashboard updated in real-time.")

        # --- Sidebar for Inputs ---
        st.sidebar.header("📝 Add an Expense")
        with st.sidebar.form("expense_form", clear_on_submit=True):
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
        
        st.sidebar.divider()

        st.sidebar.header("⚙️ Settings & Filters")
        
        if st.sidebar.button("Reset Budget"):
            st.session_state.budget = 0.0
            st.rerun()

        if st.session_state["expenses"]:
            df_for_filter = pd.DataFrame(st.session_state["expenses"])
            df_for_filter['date'] = pd.to_datetime(df_for_filter['date'])
            
            all_categories = df_for_filter['category'].unique()
            selected_categories = st.sidebar.multiselect("Filter by Category", options=all_categories, default=all_categories)

            min_date = df_for_filter['date'].min().date()
            max_date = df_for_filter['date'].max().date()
            date_range = st.sidebar.date_input("Filter by Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        
        voice_id = st.sidebar.selectbox("Select Voice", options=["en-US-natalie", "en-US-linda", "en-AU-chris", "en-GB-james"], index=0)

        st.sidebar.divider()
        if st.session_state["expenses"]:
            if st.sidebar.button("🗑️ Clear All Expenses"):
                st.session_state["expenses"] = []
                st.rerun()
        
        st.sidebar.divider()
        st.sidebar.header("🕒 Recent Activity")
        if st.session_state["expenses"]:
            for expense in st.session_state["expenses"][-5:]:
                st.sidebar.write(f"• {expense['category']}: ₹{expense['amount']:.2f}")
        else:
            st.sidebar.write("No recent activity.")


        # --- Main Page for Dashboard ---
        if st.session_state["expenses"]:
            df = pd.DataFrame(st.session_state["expenses"])
            df['date'] = pd.to_datetime(df['date'])

            # Apply filters if they exist
            if 'date_range' in locals() and len(date_range) == 2:
                start_date, end_date = date_range
                df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
            if 'selected_categories' in locals():
                df = df[df['category'].isin(selected_categories)]

            # --- Key Metrics ---
            total_spent = df["amount"].sum()
            avg_daily_spend = df.groupby(df['date'].dt.date)['amount'].sum().mean() if not df.empty else 0
            highest_expense = df['amount'].max() if not df.empty else 0
            budget_remaining = st.session_state.budget - total_spent

            st.header("Dashboard Overview", divider='rainbow')
            
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'<div class="metric-card"><h3>Total Spent</h3><p>₹{total_spent:,.2f}</p></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><h3>Budget Remaining</h3><p>₹{budget_remaining:,.2f}</p></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><h3>Average Daily Spend</h3><p>₹{avg_daily_spend:,.2f}</p></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="metric-card"><h3>Highest Expense</h3><p>₹{highest_expense:,.2f}</p></div>', unsafe_allow_html=True)

            st.subheader("Budget Progress")
            st.progress(min(total_spent / st.session_state.budget, 1.0) if st.session_state.budget > 0 else 0)

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
                if not df.empty:
                    by_category = df.groupby("category")["amount"].sum()
                    for category, amount in by_category.items():
                        summary_text += f"On {category}, you spent {amount:,.2f} rupees. "

                if st.button("🎤 Generate & Play Summary"):
                    with st.spinner("Generating voice summary..."):
                        audio_url, error = generate_voice_summary(summary_text, voice_id=voice_id)
                        if error:
                            st.error(error)
                        else:
                            st.audio(audio_url, autoplay=True)
            
            with tab2:
                st.subheader("Edit or Delete Expenses")
                edited_df = st.data_editor(
                    df, 
                    num_rows="dynamic",
                    use_container_width=True,
                    column_config={
                        "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                        "category": st.column_config.SelectboxColumn("Category", options=df['category'].unique()),
                        "amount": st.column_config.NumberColumn("Amount", format="₹%.2f")
                    }
                )
                
                if st.button("Save Changes"):
                    st.session_state["expenses"] = edited_df.to_dict('records')
                    st.success("Changes saved!")
                    st.rerun()

                st.divider()
                st.subheader("Download Data")
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Data as CSV",
                    data=csv,
                    file_name='expenses.csv',
                    mime='text/csv',
                )

        else:
            st.info("ℹ️ Add an expense using the form in the sidebar to build your dashboard.")
