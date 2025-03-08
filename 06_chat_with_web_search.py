import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
import os
import pandas as pd

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


with st.sidebar:
    api_key = st.text_input(
        #include the client key in case the user wants to see it
        "Azur OpenAI SDK Secret Key", key={subscription_key}, value={subscription_key}, type="password"
    )


    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"



if not api_key:
    api_key = subscription_key

st.title("🔎 LangChain - Chat with search")

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
        f.write(uploaded_file.getbuffer())
        # Iterate on each row
        # Extract User_Query Column value and send to llm for processing
        # Load the data
        data = pd.read_excel(file_path, engine='openpyxl')
        # Convert data to DataFrame
        df = pd.DataFrame(data)
        # Iterate on each row

        for index, row in df.iterrows():
            # Get the user query
            user_query = row['User_Query']
            # Display the user query
            st.write("User Query:", user_query)
            # Generate response
            #invoke gpt-4o-125-preview model
            llm = AzureChatOpenAI(**{'model_name': deployment, 'temperature': 0.7, 'openai_api_key': subscription_key, 
                         'azure_endpoint': endpoint, 'openai_api_version': api_version, 'streaming': False})
            #'deployment_name': 'gpt4o', 
            #llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
            response = llm.invoke(user_query)
            st.write("AI Answer:", response)
            # Display the response and write the response to the excel file under AI_answer column

            df.at[index, 'AI_Answer'] = response.content
        # Save the updated data to a new file
        new_file_path = f"./temp/{uploaded_file.name}"
        df.to_excel(new_file_path, index=False)
    # Close the file
    f.close()



"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    #llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    llm = AzureChatOpenAI(**{'model_name': deployment, 'temperature': 0.7, 'openai_api_key': subscription_key, 
                         'azure_endpoint': endpoint, 'openai_api_version': api_version, 'streaming': False})
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent(
        [search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
