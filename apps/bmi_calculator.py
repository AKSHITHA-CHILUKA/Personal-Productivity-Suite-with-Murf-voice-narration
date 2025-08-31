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
    st.title("⚖️ BMI Calculator")
    st.markdown("Calculate your Body Mass Index (BMI) to assess your weight status.")

    # --- Input form ---
    with st.form("bmi_form"):
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Enter your height (in cm)", min_value=1.0, step=1.0)
        with col2:
            weight = st.number_input("Enter your weight (in kg)", min_value=1.0, step=0.5)
        
        submitted = st.form_submit_button("Calculate BMI")

    # --- Calculation and Display ---
    if submitted:
        if height > 0 and weight > 0:
            # Convert height from cm to meters
            height_m = height / 100
            # Calculate BMI
            bmi = weight / (height_m ** 2)
            interpretation = ""

            st.subheader("Your BMI Result")
            st.metric(label="BMI", value=f"{bmi:.2f}")

            # Interpret the BMI value
            if bmi < 18.5:
                interpretation = "You are considered Underweight."
                st.warning(interpretation)
            elif 18.5 <= bmi < 25:
                interpretation = "You are considered to have a Healthy Weight."
                st.success(interpretation)
            elif 25 <= bmi < 30:
                interpretation = "You are considered Overweight."
                st.warning(interpretation)
            else:
                interpretation = "You are considered Obese."
                st.error(interpretation)
            
            if st.button("🎤 Read Result"):
                text_to_read = f"Your Body Mass Index is {bmi:.1f}. {interpretation}"
                with st.spinner("Generating audio..."):
                    audio_url, error = generate_voice(text_to_read)
                    if error:
                        st.error(error)
                    else:
                        st.audio(audio_url, autoplay=True)

            st.info("""
            **Disclaimer:** This calculator is for informational purposes only and is not a substitute for professional medical advice.
            """)
        else:
            st.error("Please enter valid height and weight values.")
