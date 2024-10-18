import random
import streamlit as st

# Initialize game state variables
if 'sequence' not in st.session_state:
    st.session_state.sequence = []
if 'user_sequence' not in st.session_state:
    st.session_state.user_sequence = []
if 'level' not in st.session_state:
    st.session_state.level = 0
if 'step' not in st.session_state:
    st.session_state.step = 'start'  # Possible steps: 'start', 'show_sequence', 'user_input', 'game_over'

# List of possible objects
objects = ['Apple', 'Banana', 'Car', 'Dog', 'Elephant']

# Function to generate a random sequence
def generate_sequence(level):
    return random.sample(objects, level)

# Function to check if user's input matches the sequence
def check_sequence():
    if st.session_state.user_sequence == st.session_state.sequence:
        st.success("Congratulations! You win!")
    else:
        st.error("Game Over! You lost.")
    st.session_state.step = 'game_over'

# Start a new game
def start_game():
    st.session_state.level = int(st.number_input("Enter difficulty level (number of objects):", min_value=1, max_value=len(objects), value=3))
    st.session_state.sequence = generate_sequence(st.session_state.level)
    st.session_state.user_sequence = []
    st.session_state.step = 'show_sequence'

# Display sequence to the user
def show_sequence():
    st.write("Memorize this sequence:")
    for obj in st.session_state.sequence:
        st.write(obj)
    if st.button("Proceed to Select"):
        st.session_state.step = 'user_input'

# Handle user input (button clicks)
def handle_input(selected_obj):
    st.session_state.user_sequence.append(selected_obj)
    if len(st.session_state.user_sequence) == len(st.session_state.sequence):
        check_sequence()

# Main app logic
st.title("Memory Game")

if st.session_state.step == 'start':
    st.write("Welcome to the Memory Game!")
    if st.button("Start Game"):
        start_game()

elif st.session_state.step == 'show_sequence':
    show_sequence()

elif st.session_state.step == 'user_input':
    st.write("Select the objects in the correct order:")
    cols = st.columns(len(objects))
    for i, obj in enumerate(objects):
        with cols[i]:
            if st.button(obj):
                handle_input(obj)

elif st.session_state.step == 'game_over':
    if st.button("Play Again"):
        st.session_state.step = 'start'
