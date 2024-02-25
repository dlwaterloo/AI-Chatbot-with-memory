import os
import random
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def configure_openai_api_key():
    # Retrieve OpenAI API Key from environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
        st.error("OpenAI API key not found in environment variables.")
        st.info("Please ensure your .env file contains the OPENAI_API_KEY variable.")
        st.stop()

# Decorator
def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):
        # To clear chat history after switching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # To show chat history on UI
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)
