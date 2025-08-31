import streamlit as st
from apps import home, expense_tracker, todo_list, bmi_calculator, pomodoro_timer, notepad, password_generator, unit_converter, interest_calculator

st.set_page_config(page_title="Personal Productivity Suite", layout="wide", page_icon="🚀")

# --- App Navigation ---
st.sidebar.title("Navigation")
app_selection = st.sidebar.radio(
    "Go to",
    ("Home", "Expense Tracker", "To-Do List", "BMI Calculator", "Pomodoro Timer", "Simple Notepad", "Password Generator", "Unit Converter", "Simple Interest Calculator")
)

# --- Load the selected app ---
if app_selection == "Home":
    home.run()
elif app_selection == "Expense Tracker":
    expense_tracker.run()
elif app_selection == "To-Do List":
    todo_list.run()
elif app_selection == "BMI Calculator":
    bmi_calculator.run()
elif app_selection == "Pomodoro Timer":
    pomodoro_timer.run()
elif app_selection == "Simple Notepad":
    notepad.run()
elif app_selection == "Password Generator":
    password_generator.run()
elif app_selection == "Unit Converter":
    unit_converter.run()
elif app_selection == "Simple Interest Calculator":
    interest_calculator.run()
