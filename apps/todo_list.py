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
    st.title("✅ Simple To-Do List")

    # Initialize session state for to-do items if it doesn't exist
    if 'todo_items' not in st.session_state:
        st.session_state.todo_items = []

    # --- Form to add new to-do items ---
    with st.form("todo_form", clear_on_submit=True):
        new_item = st.text_input("Enter a new to-do item:", placeholder="e.g., Buy groceries")
        submitted = st.form_submit_button("➕ Add Item")
        if submitted and new_item:
            st.session_state.todo_items.append({"task": new_item, "done": False})
            st.rerun()

    st.divider()

    # --- Display to-do items ---
    if not st.session_state.todo_items:
        st.info("You have no tasks. Add one above!")
    else:
        st.subheader("Your Tasks")
        for i, item in enumerate(st.session_state.todo_items):
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                # Checkbox to mark as done
                is_done = st.checkbox("", value=item["done"], key=f"done_{i}")
                st.session_state.todo_items[i]["done"] = is_done
            with col2:
                # Display task with a strikethrough if done
                task_display = f"~~{item['task']}~~" if item["done"] else item["task"]
                st.markdown(task_display, unsafe_allow_html=True)

    st.divider()

    # --- Action Buttons ---
    col1, col2 = st.columns(2)

    with col1:
        # --- Button to clear completed tasks ---
        if st.session_state.todo_items:
            if st.button("🗑️ Clear Completed Tasks", use_container_width=True):
                st.session_state.todo_items = [item for item in st.session_state.todo_items if not item["done"]]
                st.rerun()
    
    with col2:
        if st.session_state.todo_items:
            if st.button("🎤 Read My Tasks", use_container_width=True):
                tasks_to_read = [item['task'] for item in st.session_state.todo_items if not item['done']]
                if tasks_to_read:
                    text_to_read = "Here are your current tasks: " + ", ".join(tasks_to_read)
                else:
                    text_to_read = "You have no pending tasks."
                
                with st.spinner("Generating audio..."):
                    audio_url, error = generate_voice(text_to_read)
                    if error:
                        st.error(error)
                    else:
                        st.audio(audio_url, autoplay=True)
