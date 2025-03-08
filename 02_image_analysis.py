
import os
import base64
#from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

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
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
model = os.getenv("AZURE_OPENAI_LLM_4", "gpt-4o")




llm = AzureChatOpenAI(**{'model_name': 'gpt-4o', 'temperature': 0.7, 'openai_api_key': azure_openai_api_key, 
                         'azure_endpoint': endpoint, 'openai_api_version': '2024-02-01', 'deployment_name': 'gpt4o', 'streaming': False})



print(f"Deployment  : {deployment} API_version : {api_version} Endpoint : {endpoint} Key :{subscription_key} Model : {model} key : {azure_openai_api_key}")



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

def main():
    # Get initial inputs
    image_path = input("Enter path to your image: ")
    try:
        encoded_image = get_image_base64(image_path)
    except Exception as e:
        print(f"Error: {e}")
        return
    # Initialize conversation history with image
    conversation = [
        SystemMessage(content="You're a helpful assistant that can analyze images. Respond concisely."),
        HumanMessage(content=[
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            },
            {
                "type": "text",
                "text": "This is my image. I'll ask questions about it."
            }
        
        ])
    ]


    print("\nChat with the image (type 'exit' to quit)")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break

            # Add user message to conversation
            conversation.append(HumanMessage(content=user_input))

            # Get response from AzureChatOpenAI
            response = llm.invoke(conversation)
            assistant_response = response.content

            conversation.append(AIMessage(content=assistant_response))
            print(f"\nAssistant: {assistant_response}")

        except KeyboardInterrupt:
            print("\nExiting chat...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            break



if __name__ == "__main__":
    main()