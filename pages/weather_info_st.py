import streamlit as st
from weather_info import get_weather

st.title('Weather Information')

# Create a form for user input
with st.form(key='weather_form'):
    city = st.text_input('Enter city name (or type "exit" to quit): ')
    unit = st.text_input('Units (metric/imperial/kelvin, leave empty for Kelvin): ')
    submit_button = st.form_submit_button(label='Submit')

# Display the weather information on form submission
if submit_button:
    if city.lower() == 'exit':
        st.write("Goodbye!")
    else:
        weather_data = get_weather(city, unit)
        if weather_data:
            st.write(f"## {weather_data}")
        else:
            st.write("No weather data available.")
