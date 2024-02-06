import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "api")
api_port = int(os.environ.get("PORT", 8080))

# Streamlit UI elements
st.title("HEALTH TRAINER AI")

# Initial prompt for the model
initial_prompt = """
Health trainers help their clients to assess their lifestyles and wellbeing,
set goals for improving their health, agree action-plans, and provide practical
support and information that will help people to change their behaviour. 
As my Health trainer, guide me.
"""

# Send the initial prompt to the chatbot
url = f'http://{api_host}:{api_port}/'
data = {"query": initial_prompt}
initial_response = requests.post(url, json=data)

# Initialize state to keep track of conversation history
past_data = [initial_prompt, initial_response.json()]

# Display initial response
st.write("Trainer")
st.write("I am a HEALTH TRAINER AI. How can I assist you?\n")

# Streamlit callback to handle user input
@st.cache_data
def get_response(question):
    prompt = ""
    for msg in past_data:
        prompt += msg
    prompt += question
    data = {"query": prompt}
    response = requests.post(url, json=data)
    return response.json()

# Get user input
question = st.text_input(
    "You:",
    key="response",
    placeholder="Ask me anything..."
)

# Add a button to submit the response
submit_button = st.button("Ask")

# Handle button click event
if submit_button and question.strip() != "":
    # Get assistant's response and update conversation history
    response = get_response(question)
    st.write("Trainer")
    st.write(response)
    past_data.append(question)
    past_data.append(response)
