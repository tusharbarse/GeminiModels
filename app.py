from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Initiate Streamlit App

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM App")

input = st.text_input("Enter your Question: ", key="input")

submit = st.button("Ask")

if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is : ")
    st.write(response)

    