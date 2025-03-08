import streamlit as st
import dotenv
import os
import json
import time
import chardet
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
# AzureChatOpenAI API
from langchain_openai import AzureChatOpenAI
import pandas as pd
import requests
import pandas as pd
import sys
import shutil
import fitz  # PyMuPDF
#import PyMuPDF
from openai import AzureOpenAI


dotenv.load_dotenv()




# Check if the environment variables exist before deleting them
#if "http_proxy" in os.environ:
#    del os.environ["http_proxy"]
#if "https_proxy" in os.environ:
#    del os.environ["https_proxy"]

endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4-32k")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
#api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")


# Initialize Azure OpenAI Service client with key-based authentication
llm = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=api_version,
)

print(f"Endpoint: {endpoint}, Deployment: {deployment}, Subscription Key: {subscription_key}, API Version: {api_version}")


with st.sidebar:
    api_key = st.text_input(
        #include the client key in case the user wants to see it
        "Azure OpenAI SDK Secret Key", key={subscription_key}, value={subscription_key}, type="password"
    )
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/MTAGenAICourse2024/AzureOpenAISamples.git/)"

# Initialize Azure OpenAI Service client with key-based authentication
if not api_key:
    api_key = subscription_key

st.title(" 📚  Chat via RAG - Retrieval Augmented Generation Methodology")

info_on_assistant = f"ℹ️ Assistant: {deployment}"
f"""
 {info_on_assistant}
"""

# Define the  revise requirement template
answer_in_context  = """Answer the query below  {query}  in the context of the info below : {context}  and provide a response 
query : {query}
context : {context}
Answer """



# function that wrap the request to the API
def ask_llm(user_query, assistant, deployment) -> str:
    # Make sure to wait for 1 second before sending the next request
    time.sleep(1)

    #messages=[
    #                {"role": "system", "content": "You are a helpful assistant."},
    #                {"role": "user", "content": user_query},
    #        ]
  
    chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    },

    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_query
            }
        ]
    }
    ]

    completion = assistant.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
    response = completion.choices[0].message
    
    return response.content

    
def pdf_to_text(file_path):
    # Open the PDF file

    # Check if file_path is None or not a string
    if file_path is None or not isinstance(file_path, str):
        raise ValueError("The file_path must be a valid string representing the path to the file.")

    # Print the file_path for debugging
    print(f"file_path: {file_path}")

    # Get the absolute path of the file
    absolute_file_path = os.path.abspath(file_path)

    # Check if the file exists
    if not os.path.exists(absolute_file_path):
        raise FileNotFoundError(f"The file {absolute_file_path} does not exist.")

    pdf_document = fitz.open(absolute_file_path)
    text = ""

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        print(f'Page num : {page_num}')
        text += page.get_text()

    return text


# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

# Read documents from the directory
documents_dir = "data/RAG/"
documents = []
filenames = []
for filename in os.listdir(documents_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(documents_dir, filename)
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
            documents.append(file.read())
            filenames.append(filename)

# Step 1: Vectorize the documents using TF-IDF
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(documents).toarray()

# Step 2: Build a FAISS index for efficient similarity search
index = faiss.IndexFlatL2(doc_vectors.shape[1])
index.add(doc_vectors)

def retrieve_relevant_docs(query, k=2):
    query_vector = vectorizer.transform([query]).toarray()
    distances, indices = index.search(query_vector, k)
    return [documents[i] for i in indices[0]]


def retrieve_context(input_text):

    relevant_docs = retrieve_relevant_docs(input_text)
    context = " ".join(relevant_docs)
    return(context)


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, Ask me any question on Trivia "}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Which film won 2025 Best Film Award in Oscars?"):
    context = retrieve_context(prompt)
    prompt_with_context = answer_in_context.format(
        query=prompt,
        context=context
    )
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        response = ask_llm(prompt_with_context, llm, deployment)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

