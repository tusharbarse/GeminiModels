from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(promt, image, input):
    response = model.generate_content([promt, image, input])
    return response

st.set_page_config(page_title="MultiLanguage Information Extractor")

st.header("MultiLanguage Information Extractor")

input = st.text_input("Input")

upload_image = st.file_uploader("Selet Image", type=["png", "jpg", "jpeg"])
image = ""
if upload_image:
    image = Image.open(upload_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Ask you Question")

prompt = """You are expert in unserstanding invoices, you will receive image as an invoice
and query regarding invoice you have to answer query in response """

if submit and input:
    respose = get_gemini_response(prompt, image, input)
    st.subheader("Response: ")
    st.write(respose.text)
    # st.write(upload_image.getvalue())


