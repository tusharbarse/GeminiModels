from dotenv import load_dotenv
import os 
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

from langchain_community.vectorstores import FAISS


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectore_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("FAISS_DATA")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from provided context,
    make sure to provide details as much as possible,
    if answer is not in context then just say "answer not within context" 
    do not provide wrong answer\n\n
    Context : {context}
    Question : {question}
    Answer : 
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temparature=0.4)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "questtion"])
    chain = load_qa_chain(model, prompt=prompt)
    return chain

def ask_query(user_input):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("FAISS_DATA", embeddings=embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_input)

    chain = get_conversational_chain()

    response = chain({"input_documents":docs, "question":user_input})
    print(response)
    st.write(response['output_text'])

st.set_page_config("Chat PDF")
st.header("RAG using GEMINI")

user_input = st.text_input("Enter Query")

if user_input:
    ask_query(user_input)

with st.sidebar:
    st.title("Menu: ")
    pdf_docs = st.file_uploader("Select PDF Docs..", type=["pdf"], accept_multiple_files=True)
    if st.button("Submit & Process") and pdf_docs:
        with st.spinner("Processing"):
            text = get_pdf_text(pdf_docs)
            chunks = get_chunk_text(text)
            get_vectore_store(chunks)
            st.write("Done")
            


