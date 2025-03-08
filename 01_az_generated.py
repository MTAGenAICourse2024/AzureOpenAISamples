
import os
import base64
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4-32k")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
#api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

# Initialize Azure OpenAI Service client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=api_version,
)


# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# Prepare the chat prompt
user_input = input("Please enter your prompt: ")
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
                "text": user_input
            }
        ]
    }
]

# Include speech result if speech is enabled
messages = chat_prompt

# Generate the completion
completion = client.chat.completions.create(
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

print(completion.to_json())


# Now let's see the result:
print(completion.model_dump_json(indent=3))

# And specifically just the answer from the LLM:
print("-" * 40, "\nResponse from LLM:\n")
print(completion.choices[0].message.content)
print("\n", "-" * 40)
print(f"$ prompt_tokens: {completion.usage.prompt_tokens}")
print(f"$ completion_tokens: {completion.usage.completion_tokens}")
print(f"$ total_tokens: {completion.usage.total_tokens}")
print("-" * 40, "\n")

