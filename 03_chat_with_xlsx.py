import streamlit as st
import os
import pandas as pd
import dotenv
from openai import AzureOpenAI
import requests
import os
import json
import time
import sys

dotenv.load_dotenv()

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


# function that wrap the request to the API
def ask_llm(user_query, assistant, deployment) -> str:
    # Make sure to wait for 1 second before sending the next request
    time.sleep(1)

    #messages=[
    #                {"role": "system", "content": "You are a helpful assistant."},
    #                {"role": "user", "content": user_query},
    #        ]
    print(f" In side ask_llm function")
    print(f"Endpoint: {endpoint}, Deployment: {deployment}, Subscription Key: {subscription_key}, API Version: {api_version}")
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

    




# Check if the environment variables exist before deleting them
#if "http_proxy" in os.environ:
#    del os.environ["http_proxy"]
#if "https_proxy" in os.environ:
#    del os.environ["https_proxy"]

with st.sidebar:
    api_key = st.text_input(
        #include the client key in case the user wants to see it
        "Azure OpenAI Key", key={subscription_key}, value={subscription_key}, type="password"
    )
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/MTAGenAICourse2024/AzureOpenAISamples.git/)"




st.title("🔎 Q&A in xlsx ")
info_on_assistant = f"ℹ️ Assistant: {deployment}"
f"""
 {info_on_assistant}
"""
#Add option to read in an excel file including questions and answers
#st.write("Upload a file with questions and answers")

# File uploader
uploaded_file = st.file_uploader("Choose an xlsx file...", type=[ "csv", "xlsx"])

if uploaded_file is not None:
    # Ensure the temp directory exists
    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)
    # Copy the file to the temp directory
    file_path = f"./temp/{uploaded_file.name}"
    with open(file_path, "wb") as f:

        
        if not api_key:
            st.info("Please add your Azure OpenAI API key to continue.")
            st.stop()
        
        llm = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=subscription_key,
            api_version=api_version,
        )
  


        f.write(uploaded_file.getbuffer())
        data = pd.read_excel(file_path, engine='openpyxl')
        # Convert data to DataFrame
        df = pd.DataFrame(data)
        # Iterate on each row
        for index, row in df.iterrows():
            # Get the user query
            user_query = row['User_Query']
            # Display the user query
            st.write("Answering User Query:", user_query)
            # Generate response
            #invoke gpt-4o-125-preview model
          

            response = ask_llm(user_query, llm, deployment)
            

            # Display the response and write the response to the excel file under AI_answer column
            #Create a name for the column including the ChAI use case
            column_name = f"AI_Answer"
            df.at[index, column_name] = response
        # Save the updated data to a new file
        new_file_path = f"./temp/{uploaded_file.name}"
        df.to_excel(new_file_path, index=False)

        completion_text = f"Completed updating the xls and copied to temp subdirectory with answers from AI"
        highlighted_content = f'<span style="background-color: blue;">{completion_text}</span><br>'
        # Use st.markdown to display the content in a scrollable text area
        st.markdown(
            f'<div style="overflow-y: auto; height: 50px; border: 1px solid #ccc; padding: 10px;">{highlighted_content}</div>',
            unsafe_allow_html=True)



    # Close the file
    f.close()


