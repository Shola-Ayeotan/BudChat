import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Welcome to BudChat!")
st.write(
    "Think of me as your go-to gist partner. \n"
    "Whether you're looking for advice, need help with simple tasks, \n"
    "or just want to chat about your day, BudChat is here to listen and support you. \n"
)

# Retrieve the OpenAI API key from secrets.
openai_api_key = st.secrets["openai"]["api_key"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a footer credit immediately after the chat input area.
st.markdown("---")  # Horizontal line for separation
st.write("Created by Shola Ayeotan © 2024")
