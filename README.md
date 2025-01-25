# AzureOpenAISamples
Sample Streamlit applications showcasing usage of AzureOpen AI 
#PowerShell script to set the OpenAI API key as an environment variable

# Set the OpenAI API key
$env:OPENAI_API_VERSION="2024-05-01-preview"
$env:AZURE_OPENAI_LLM_35="gpt-35-turbo"

# GPT-4o Specific Parameters
$env:AZURE_OPENAI_API_VERSION="2024-02-15-preview"
$env:AZURE_OPENAI_LLM_4="gpt-4o"

# Global Parameters  - These info can be extracted from your Azure personal account 
$env:AZURE_OPENAI_ENDPOINT=  <Your Endpoint>
$env:AZURE_OPENAI_API_KEY=  <Your key>

#Invoke the app to run interactively the ChATbot using the right engine
Streamlit run Chatbot.py 
![AzureOpenAIAccount](https://github.com/user-attachments/assets/ae83bcf8-1483-4711-9fbb-aaab1b695321)
