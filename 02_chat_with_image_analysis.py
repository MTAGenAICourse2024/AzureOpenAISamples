import os
import base64
import streamlit as st
#from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Delete proxy settings if they exist
if "http_proxy" in os.environ:
   print(f"Deleting http_proxy: {os.environ['http_proxy']}")
   del os.environ["http_proxy"]

if "https_proxy" in os.environ:
    print(f"Deleting https_proxy: {os.environ['https_proxy']}")
    del os.environ["https_proxy"]


endpoint = os.getenv("ChAI_ENDPOINT_URL", "https://gptturbo.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")

subscription_key = os.getenv("ChAI_AZURE_OPENAI_API_KEY")
azure_openai_api_key = subscription_key
api_version = os.getenv("ChAI_AZURE_OPENAI_API_VERSION", "2024-02-01")
model = os.getenv("AZURE_OPENAI_LLM_4", "gpt-4o")




llm = AzureChatOpenAI(**{'model_name': 'gpt-4o', 'temperature': 0.7, 'openai_api_key': azure_openai_api_key, 
                         'azure_endpoint': endpoint, 'openai_api_version': '2024-02-01', 'deployment_name': 'gpt4o', 'streaming': False})



print(f"API_version : {api_version} Endpoint : {endpoint} Key :{subscription_key} Model : {model} key : {azure_openai_api_key}")



def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    return encoded_image

def get_image_base64(image_path: str) -> str:
    """Validate and encode image to base64"""
    #image_path = image_path.strip('"\'').strip()
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")
    
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("ascii")
    

def create_conversation_with_image(encoded_image, prompt) :
    # Initialize conversation history with image
    conversation = [
        SystemMessage(content="You're a helpful assistant that can analyze images. Respond concisely. Make sure that your textual responses leverage punctuation and natural language for better intonation by text to speech TTS engines."),
        HumanMessage(content=[
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            },
            {
                "type": "text",
                "text": "This is my image. I'll ask questions about it"
            }
        ])
    ]
    return conversation




def single_image_analysis(image_path):
    # Get initial inputs
    global llm

    # Display the uploaded image
    image = Image.open(image_path)
    #st.image(image, caption='Uploaded Image')
    encoded_image = get_image_base64(image_path)

    describe_image_prompt = "Describe what is seen in the image in detail"

    conversation = create_conversation_with_image(encoded_image, describe_image_prompt)
    # Add user message to conversation
    conversation.append(HumanMessage(content=describe_image_prompt))
    # Get response from AzureChatOpenAI
    try:
        response = llm.invoke(conversation)
        image_description = response.content
    except Exception as e:
        print(f"Error invoking AzureChatOpenAI: {e}")
        return None

    # Clear previous messages
    st.session_state.messages = []

    
    # Display the image
    image_caption = "Uploaded Image"
    st.image(image, caption=image_caption)
    conversation.append(HumanMessage(content=describe_image_prompt))
 
   
    response = llm.invoke(conversation)
    image_description = response.content

    st.write("Below you can find a description of the uploaded image :")
    st.write(image_description)
    
    #if tts_on and 'tts_initialized' not in st.session_state:
    #    tts = TTSManager()
    #    try:
    #        tts.add_to_tts(image_description)
    #        print(f"tts_on: {tts_on}")
    #        tts.start_tts()
    #        st.session_state['tts_initialized'] = True
    #    except ValueError as e:
    #        st.error(f"TTS Manager Error: {e}")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can assist you analyze the image that you have uploaded. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Can you describe the image in detail?"):
         # Clear previous messages
        st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        conversation.append(HumanMessage(content=prompt))  
        response = llm.invoke(conversation)
        image_description = response.content

        with st.chat_message("assistant"):
             # Add user message to conversation
            
            st.session_state.messages.append({"role": "assistant", "content": image_description})
            st.write(image_description)
            #if tts_on:
            #    tts = TTSManager()
            #    try:
            #        tts.add_to_tts(image_description)
            #        print(f"tts_on: {tts_on}")
            #        tts.start_tts()
            #        st.session_state['tts_initialized'] = True
            #    except ValueError as e:
            #        st.error(f"TTS Manager Error: {e}")
                 
            
    
       
    
    return image_description

    

st.title("🖼️ Q&A with Images ")
f"""
    Leverages a gpt 4o model  to  answer a question related with an image  
   """
image = st.file_uploader(
    "Choose a picture to analyze ...", type=["jpg", "jpeg", "png"])

with st.sidebar:
    api_key = st.text_input(
        #include the client key in case the user wants to see it

        "Azure Open API  Secret Key", key={subscription_key}, value={subscription_key}, type="password"
    )
"[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/MTAGenAICourse2024/AzureOpenAISamples.git/)"
 


        
def main():
    global image

    if image is not None:
        print(f"image_path: {image.name}")
        #Get the full path 
        #image_path = os.path.abspath(image.name)
        os.makedirs("./temp", exist_ok=True)

        image_path = f"./temp/{image.name}"
        print(f"Absolute_path : {image_path}")
        with open(image_path, "wb") as temp_img_f:
            #Copy the file to the temp directory
           
            temp_img_f.write(image.getbuffer())
            image_description = single_image_analysis(image_path)   





if __name__ == "__main__":
    main()