import streamlit as st
from openai import OpenAI
from pathlib import Path

st.set_page_config(page_title="AI Chatbot", page_icon=":speech_balloon:")
st.markdown(f"<style>{Path('style.css').read_text()}</style>", unsafe_allow_html=True)

with st.sidebar :
    api_key = st.text_input("OpenAI API Key", type="password")
    if st.button("clear chat"):
        st.session_state.messages = []
        
st.title("AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
if prompt := st.chat_input("Type your message here..."):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    client = OpenAI(api_key=api_key)
    with st.chat_message("assistant") :
        placeholder = st.empty()
        reply = ""
        for chunk in client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages, stream=True) :
            chunk_message = chunk.choices[0].delta.content
            reply += chunk.choices[0].delta.content or ""
            placeholder.markdown(reply + "▌")
        placeholder.markdown(reply)
        
    st.session_state.messages.append({"role": "assistant", "content": reply})
        