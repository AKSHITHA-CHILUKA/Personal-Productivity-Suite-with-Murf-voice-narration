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
    st.title("📈 Simple Interest Calculator")
    st.markdown("Calculate the simple interest on a loan or investment.")

    with st.form("interest_form"):
        principal = st.number_input("Principal Amount (₹)", min_value=0.0, format="%.2f")
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, format="%.2f")
        time = st.number_input("Time Period (in years)", min_value=0.0, format="%.1f")
        
        submitted = st.form_submit_button("Calculate Interest")

    if submitted:
        if principal > 0 and rate > 0 and time > 0:
            # Calculate simple interest
            interest = (principal * rate * time) / 100
            total_amount = principal + interest

            st.subheader("Calculation Result")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Interest", f"₹{interest:,.2f}")
            with col2:
                st.metric("Total Amount", f"₹{total_amount:,.2f}")

            if st.button("🎤 Read Result"):
                text_to_read = f"For a principal of {principal:,.2f} rupees at an annual rate of {rate} percent for {time} years, the total interest is {interest:,.2f} rupees, making the total amount {total_amount:,.2f} rupees."
                with st.spinner("Generating audio..."):
                    audio_url, error = generate_voice(text_to_read)
                    if error:
                        st.error(error)
                    else:
                        st.audio(audio_url, autoplay=True)
        else:
            st.error("Please enter valid values for principal, rate, and time.")
