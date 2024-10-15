import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("✝️ Welcome to FaithBud!")
st.write(
    "I am FaithBud, your personal AI assistant created to help you grow in your relationship with God. \n\n"
    
    "Whether you're seeking guidance, have questions about certain Scriptures, \n"
    "or simply want to discuss your faith journey, I'm here to listen and support you. \n"
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
if prompt := st.chat_input("How can I help you grow in faith today?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        max_tokens=200,  # Adjust this based on desired response length
        temperature=0.7,  # Adjust for more creative responses
    )

    # Extract the assistant's response correctly.
    assistant_response = response.choices[0].message['content']

    # Stream the response to the chat.
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Add a footer credit immediately after the chat input area.
st.markdown("---")  # Horizontal line for separation
st.write("Oluwanishola Ayeotan © 2024")
