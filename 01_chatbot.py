import streamlit as st
# AzureChatOpenAI API
#from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI
import os
import dotenv

dotenv.load_dotenv()

# Check if the environment variables exist before deleting them
#if "http_proxy" in os.environ:
#    del os.environ["http_proxy"]
#if "https_proxy" in os.environ:
#    del os.environ["https_proxy"]


endpoint = os.getenv("ENDPOINT_URL", "https://gilak-m7vuff9p-swedencentral.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4-32k")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "C9NYG6dTbxV1HdWXj8VK71IeJVhhT3k2FC4Rta7udcBfiUKq69SnJQQJ99BCACfhMk5XJ3w3AAAAACOGwIub")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")

# Initialize Azure OpenAI Service client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=api_version,
)

print(f"Endpoint: {endpoint}, Deployment: {deployment}, Subscription Key: {subscription_key}, API Version: {api_version}")

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')




with st.sidebar:
    api_key = st.text_input(
        #include the client key in case the user wants to see it
        "ChAI Client SDK Secret Key", key={subscription_key}, value={subscription_key}, type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"



# Initialize Azure OpenAI Service client with key-based authentication

if not api_key:
    api_key = subscription_key

st.title("Chat Q & A ")

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

if prompt := st.chat_input(placeholder="Can you please suggest a good book to read over the weekend ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your Azure OpenAI API key to continue.")
        st.stop()

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version=api_version,
    )
  



    with st.chat_message("assistant"):
        #st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        # Generate the completion
        completion = client.chat.completions.create(
            model=deployment,
            messages=st.session_state.messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )

        #response = client.invoke(st.session_state.messages)
        response = completion.choices[0].message
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        st.write(response.content)
        #st.chat_message("assistant").write(response.content)
