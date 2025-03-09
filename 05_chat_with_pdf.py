import streamlit as st
# AzureChatOpenAI API
from langchain_openai import AzureChatOpenAI
import os
import pandas as pd
import dotenv
import requests
import json
import pandas as pd
import time
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

st.title("📄 Chat with AI assistant referencing a document ")
info_on_assistant = f"ℹ️ Assistant: {deployment}   - In this version the answers are provided while referncing a document."
f"""
 {info_on_assistant}
"""



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



# Example usage
#file_path = "example.pdf"
#text = pdf_to_text(file_path)
#print(text)




# Check if the environment variables exist before deleting them
#if "http_proxy" in os.environ:
#    del os.environ["http_proxy"]
#if "https_proxy" in os.environ:
#    del os.environ["https_proxy"]


max_tokens = 30000



# Create tenplate with query and content
answer_referencing_doc_template = """ Answer the user query {query} by referencing the content  {content} 
query : {query}
content : {content}
Response : """



def answer_referencing_doc(prompt, content, assistant, deployment):
    #Answer referencing the content read from a doc (pdf or docx)

    response = None
    size = len(content)
    print(f"Size of the doc is {size}")

    if prompt is not None:

        if (len(content) < max_tokens) :
            formatted_template = answer_referencing_doc_template.format(
                query=prompt,
                content=content
            )

            response = ask_llm(formatted_template, assistant, deployment)
            print(f'Answer for user query : {prompt}  is   {response}')
            # st.write('Checked the compliance of spec with design rule : ', design_rule)

        else:
            #st.session_state.messages.append({"role": "assistant", "content": response})
            st.write("The doc is too large, consider breaking it  into chunks or leverage RAG methodology to take care of your files")
            print(f"The doc is too large, consider breaking it  into chunks or leverage RAG methodology to take care of your files")

    return response



def create_conversation_referencing_doc(content, assistant, deployment):
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm a chatbot who can provide you  and answer referencing the doc that you provided. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Who are the authors of the doc ? "):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)


        with st.chat_message("assistant"):

            response = answer_referencing_doc(prompt, content, assistant, deployment)
            if response is not None:
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
            else:
                st.write("No response from the assistant. Most probably the doc is too large. Consider creating an exploratory ChAI use case and uploading your files")



uploaded_doc = st.file_uploader("Choose a pdf file to reference while answering questions ...", type=["pdf"])

spec_text = ""
if uploaded_doc is not None:
    # Ensure the temp directory exists
    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)
    # Copy the file to the temp directory

    spec_file_path = f"./temp/{uploaded_doc.name}"
    with open(spec_file_path, "wb") as temp_spec_f:
        temp_spec_f.write(uploaded_doc.getbuffer())
    spec_text = pdf_to_text(spec_file_path)


    #print(f'Spec text : {spec_text}')

    if spec_text is not None:
        print(f"Assistant : {deployment}")
        print(f"I will answer leveraging the file {uploaded_doc.name} and also ChAI assistant {deployment} knowledge")
    else:
        print(f'No doc has been fed in')
        st.write('No pdf has been fed in. Note that your query will be answered only via knowledge of ChAI assistant {deployment} with no extra doc.')

    create_conversation_referencing_doc(spec_text, llm, deployment)





