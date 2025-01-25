import streamlit as st
# AzureChatOpenAI API
from langchain_openai import AzureChatOpenAI
import os
import dotenv

dotenv.load_dotenv()

# Check if the environment variables exist before deleting them
if "http_proxy" in os.environ:
    del os.environ["http_proxy"]
if "https_proxy" in os.environ:
    del os.environ["https_proxy"]


with st.sidebar:
    api_key = st.text_input(
        "AzureOpenAI API Key", key="langchain_search_api_key_openai", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


#azure_deployment = os.getenv["AZURE_OPENAI_LLM_35"]
azure_deployment = os.getenv("AZURE_OPENAI_LLM_35")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")


if not api_key:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

st.title("🔎 Chat (No Web Access)")




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
    llm = AzureChatOpenAI(
        openai_api_key=api_key,
        azure_deployment=azure_deployment,
        openai_api_version=api_version
    )

    #llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)



    with st.chat_message("assistant"):
        #st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        st.write(response.content)
        #st.chat_message("assistant").write(response.content)
