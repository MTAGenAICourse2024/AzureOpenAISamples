import streamlit as st
import os
import requests
import json
import time
import shutil
import sys
from openai import AzureOpenAI
import dotenv
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
        "Azure OpenAI Key", key={subscription_key}, value={subscription_key}, type="password"
    )
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/MTAGenAICourse2024/AzureOpenAISamples.git/)"


# Initialize Azure OpenAI Service client with key-based authentication

if not api_key:
    api_key = subscription_key


st.title("💬 Dialogue with AI assistant ")
info_on_assistant = f"ℹ️ Assistant: {deployment}   - In this version, the answers are aware of all the context of the conversation"
f"""
 {info_on_assistant}
"""

# function that wrap the request to the API
def ask_llm(messages, assistant, deployment) -> str:
    # Make sure to wait for 1 second before sending the next request
    time.sleep(1)
    
    completion = assistant.chat.completions.create(
            model=deployment,
            messages=messages,
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




# define the prompt for the iterative questions, that will appear in each iteration
iterative_prompt = """You are an AI Assistant and you're asked questions in an iterative manner. \
                    In each step, the previous answer and the follow-up question are given. \
                    Answer the current question and take the last answer under consideration\n"""


# define the prompts for the previous and next questions
previous_step_prompt = "This is the last answer:\n"
next_step_prompt = "This is the current question:\n"
last_output = " "



if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can assist you with general questions. I have a good memory. I remember the context of our conversation while answering you. How can I help you?"}
    ]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is the capital of France?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # in each iteration ask the question and print the answer
        # the answer of the previous question is added to the prompt of the next question
        current_prompt = iterative_prompt + last_output + next_step_prompt + prompt

        last_output = ask_llm(st.session_state.messages, llm, deployment)
        st.session_state.messages.append({"role": "assistant", "content": last_output})
        st.write(last_output)

