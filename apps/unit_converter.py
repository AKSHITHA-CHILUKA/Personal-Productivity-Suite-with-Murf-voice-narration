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

# --- Conversion Logic ---
CONVERSION_FACTORS = {
    "Length": {"Meters": 1.0, "Kilometers": 1000.0, "Feet": 0.3048, "Miles": 1609.34},
    "Weight": {"Grams": 1.0, "Kilograms": 1000.0, "Pounds": 453.592, "Ounces": 28.3495},
    "Temperature": {} # Special case
}

def convert_units(value, from_unit, to_unit, category):
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        else:
            return value # No conversion needed
    else:
        base_value = value * CONVERSION_FACTORS[category][from_unit]
        return base_value / CONVERSION_FACTORS[category][to_unit]

def run():
    st.title("🔄 Unit Converter")
    st.markdown("Quickly convert between common units of measurement.")

    category = st.selectbox("Select Conversion Type", ("Length", "Weight", "Temperature"))

    if category == "Temperature":
        units = ["Celsius", "Fahrenheit"]
    else:
        units = list(CONVERSION_FACTORS[category].keys())

    col1, col2, col3 = st.columns(3)
    with col1:
        value_to_convert = st.number_input("Value", value=1.0)
    with col2:
        from_unit = st.selectbox("From", units, index=0)
    with col3:
        to_unit = st.selectbox("To", units, index=1)

    result = convert_units(value_to_convert, from_unit, to_unit, category)

    st.subheader("Result")
    st.metric(label=f"{value_to_convert} {from_unit} is", value=f"{result:,.4f} {to_unit}")

    if st.button("🎤 Read Result"):
        text_to_read = f"{value_to_convert} {from_unit} is equal to {result:,.2f} {to_unit}"
        with st.spinner("Generating audio..."):
            audio_url, error = generate_voice(text_to_read)
            if error:
                st.error(error)
            else:
                st.audio(audio_url, autoplay=True)
