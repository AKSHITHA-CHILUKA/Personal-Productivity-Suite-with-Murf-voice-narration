import streamlit as st
import random
import string
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

def generate_password(length, use_uppercase, use_numbers, use_symbols):
    """Generate a random password based on user criteria."""
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    if not characters:
        return "Please select at least one character type."
        
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def run():
    st.title("🔐 Secure Password Generator")
    st.markdown("Create strong, random passwords to keep your accounts secure.")

    # --- Password Options ---
    st.subheader("Password Options")
    length = st.slider("Password Length", min_value=8, max_value=64, value=16)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        use_uppercase = st.checkbox("Include Uppercase (A-Z)", value=True)
    with col2:
        use_numbers = st.checkbox("Include Numbers (0-9)", value=True)
    with col3:
        use_symbols = st.checkbox("Include Symbols (!@#$)", value=True)

    # --- Generate and Display Password ---
    if st.button("Generate Password", use_container_width=True):
        password = generate_password(length, use_uppercase, use_numbers, use_symbols)
        st.session_state.generated_password = password

    if "generated_password" in st.session_state and st.session_state.generated_password:
        st.subheader("Your New Password")
        st.code(st.session_state.generated_password)
        
        if st.button("🎤 Read Password Aloud"):
            # Format password to be read clearly
            readable_password = " ".join(list(st.session_state.generated_password))
            text_to_read = f"Your password is: {readable_password}"
            with st.spinner("Generating audio..."):
                audio_url, error = generate_voice(text_to_read)
                if error:
                    st.error(error)
                else:
                    st.audio(audio_url, autoplay=True)
