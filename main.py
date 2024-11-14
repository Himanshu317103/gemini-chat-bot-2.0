import time
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'

    # Start chat with Generative AI model
    st.session_state.model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history, )

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(
                name=message['role'],
                avatar=message.get('avatar'),
        ):
            st.markdown(message['content'])

    # Get user input
    st.sidebar.subheader(" ")
    st.sidebar.image(r"pngwing.com.png")
    prompt = st.sidebar.text_input('Ask any question...')

    txt = """Cypher is an advanced chatbot designed to provide accurate and helpful information on various diseases, including Diabetes, Heart Diseases, Kidney Diseases, and more. 
            Whether you have questions about symptoms, treatments, or prevention strategies, Cypher is here to assist you."""
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

        # Send message to AI and get response (stream for animation)
        query = f"""
            Remember all these-
            1. your name is Cypher and you are an assiatant created by Himanshu sharma and your job is to answer all the question related to  all kind of  disease.
            2. don't mention about you are created by google or your name is gemini anywhere.
            3. answer all question in brief untill asked for detailed explanation.
            4. please make sure to mention symptoms,cause ,precaution,medication in organized manner.
            5. if user asked anything outside of the scope of health diseases then tell them that i don't know that ask me question related to machine Learning only.

            make sure you follow all the above rules.
            question - {prompt}
        """
        response = st.session_state.chat.send_message(
            query,
            stream=True,
        )

        # Display assistant response in chat message container
        with st.chat_message(
                name='AI',
                avatar='👁️',
        ):
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

        # Clear the sidebar input after processing
        st.session_state.user_input = ''  # Clear the input using session state


chat()
