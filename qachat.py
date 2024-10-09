from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel("gemini-1.5-flash")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'history' not in st.session_state:
    st.session_state['history'] = []

# print(history)
chat = model.start_chat(history=st.session_state['history'])

def get_gemini_response(input):
    response = chat.send_message(input, stream=True)
    return response

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Chat Application")

input = st.text_input("Input: ", )
submit = st.button("Ask the Question")


if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    complete_response = ""
    for chunk in response:
        st.write(chunk.text)
        complete_response += chunk.text
    st.session_state['chat_history'].append(("Bot", complete_response))

if st.session_state['chat_history']:
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role} : {text}")
    print(chat.history)
    st.session_state['history'].extend(chat.history)