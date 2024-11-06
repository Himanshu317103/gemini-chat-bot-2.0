import time
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

api_key = "AIzaSyC5RrLxZ9Pct-W2OGP8pL0wKLl81-fYvnU"

# Initialize the AI model with the API key
genai.configure(api_key=api_key)

st.markdown("""
    <style>
        .st-emotion-cache-139wi93, st-emotion-cache-vj1c9o ea3mdgi6 {
            padding-left: 0rem;
            padding-right: 0rem;
            width: 100%;
            padding: 0rem 0rem 0px;
            max-width: 100%;
        }
    </style>
""", unsafe_allow_html=True)


def chat():
    """
    Function to handle chat interaction with the Generative AI model.

    - Initializes session variables if not already set.
    - Starts a chat session with the generative AI model.
    - Displays past chat messages from history on app rerun.
    - Gets user input and processes it with the AI model.
    - Streams the AI response and displays it in the chat interface.
    - Updates chat history with both user and AI messages.
    """

    # Initialize session variables
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'gemini_history' not in st.session_state:
        st.session_state.gemini_history = []

    # Start chat with Generative AI model
    st.session_state.model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(name=message['role'], avatar=message.get('avatar')):
            st.markdown(message['content'])

    # Get user input
    prompt = st.sidebar.chat_input('Ask any question...')

    # Info about the chatbot in the sidebar
    txt = """Baymax is an advanced chatbot designed to provide accurate and helpful information on various diseases, including Diabetes, Heart Diseases, Kidney Diseases, and more.
            Whether you have questions about symptoms, treatments, or prevention strategies, Baymax is here to assist you."""
    st.sidebar.info(txt)

    # Process user input and AI response
    if prompt:
        # Display user message in chat message container
        with st.chat_message('User'):
            st.markdown(str.capitalize(prompt))

        # Add user message to chat history
        st.session_state.messages.append(
            dict(
                role='User',
                content=prompt,
            )
        )

        # Prepare the AI query with predefined instructions
        query = f"""
            1. Your name is Baymax and you are an assistant created by Harshit Pathak. Your job is to answer questions related to diseases like diabetes, Alzheimer's, Heart Diseases, Kidney diseases, etc.
            2. Do not mention that you're created by Google or that your name is Gemini.
            3. Answer all questions in brief unless asked for a detailed explanation.
            4. If the user asks anything outside of the scope of health diseases, tell them that you don't know, and ask them to ask about machine learning only.

            Question: {prompt}
        """

        # Send message to AI and get response (stream for animation)
        response = st.session_state.chat.send_message(query, stream=True)

        # Display assistant response in chat message container
        with st.chat_message('AI', avatar='✨'):
            message_placeholder = st.empty()
            full_response = ''

            # Stream in AI response with character-by-character animation
            for chunk in response:
                for ch in chunk.text.split(' '):
                    full_response += ch + ' '
                    time.sleep(0.05)  # Adjust delay for desired typing animation speed
                message_placeholder.write(full_response + '▌')
            message_placeholder.write(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            dict(
                role='AI',
                content=st.session_state.chat.history[-1].parts[0].text,
                avatar='✨',
            )
        )

    # Clear the sidebar input after processing (handled directly in the widget)
    st.session_state.messages = []  # Clear the session state for new user input


# Run the chat function
chat()
