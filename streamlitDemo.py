import os
import sys
import streamlit as st
from llamaindex import LlamaIndex
from crawler import Crawler
from chatgpt import ChatGPT

OPENAI_API_KEY = 'sk-' # implement your own API_KEY from OPENAI
GPT_MODEL = 'gpt-3.5-turbo'

csv_file_path = "demo.csv"
index_save_path = "index/"
collection_name = "APCalculus"

@st.cache_resource
def initLlamaIndex():
    llamaindex = LlamaIndex(OPENAI_API_KEY,GPT_MODEL)
    llamaindex.importCSVFile(csv_file_path)
    llamaindex.buildIndex(index_save_path,collection_name)
    return llamaindex

llamaindex = initLlamaIndex()

st.markdown("Input a question about AP calculus. Output related topic notes.")
st.markdown("Source: https://www.studypug.com/ap-calculus-bc")
st.header("Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hi, I'm your AI assistant. Any question on AP calculus?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if stQuestion := st.chat_input("Send a message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": stQuestion})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(stQuestion)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        node = llamaindex.retrieveTopicNotes(stQuestion)[0]

        summary = "Summary: "+node.node.metadata["summary"]
        st.markdown(summary)

        full_response = "Details: "+node.text
        st.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": summary})
    st.session_state.messages.append({"role": "assistant", "content": full_response})
