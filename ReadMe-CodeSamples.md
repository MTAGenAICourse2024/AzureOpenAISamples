# Azure Open AI SDK Code Samples 

This directory includes code samples that show usage of  Azure Open AI SDK 

1. **Chat bot - textual :** Enable via an Open AI model (gpt-4-32k) to conduct a textual dialogue (include a Streamlit UI interface)
2. **Chat bot - textual / visual :** Enable via an Open AI model (gpt-4o) to ask questions about an image (include a Streamlit UI interface)
3. **Chat via xls (Read in Qs / Write As) :** Read in questions from xls file and provide answers in a new column
4. **Conversation-aware Bot :** Enable conversation aware dialogue leveraging a specific OpenAI model
5. **Chat with a doc (pdf) :** Ask questions on a specific pdf 
6. **Agentic Flow (get answer from Web or General Knowledge):** Get answer from Web or General Knowledge leveraging agents provided via LangChain framework 
7. **Chat leveraging new knowledge (simple RAG):** Answer questions while retrieving relevant documets to answer

## Prerequisites

Before running any of the scripts, make sure you have the following:

- Python 3.11 or higher
- Required Python packages (see below for installation instructions)
- Make sure that you have installed the requirements

Build a virtual environment 
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

```bash
pip install -r requirements.txt
```
- Make sure that .env includes and you have  set the environment variables
- Refer to README.md 
   ```bash
   ENDPOINT_URL=<YOUR ENDPOINT URL>
   DEPLOYMENT_NAME="gpt-4-32k"
   AZURE_OPENAI_API_KEY=<YOUR API KEY>
   AZURE_OPENAI_LLM_35="gpt-35-turbo"
   AZURE_OPENAI_API_VERSION="2025-01-01-preview"
   AZURE_OPENAI_LLM_4="gpt-4"
   ```



## I. Chat bot - textual 

**Purpose:** Enable via an Open AI model (gpt-4-32k) to conduct a textual dialogue (include a Streamlit UI interface)

**Usage:**
1. Command line execution 
```python
python .\01_az_generated.py
```
2. Jupyter noetbook execution 

To run  in a Jupyter Notebook, you can use the following code snippet: [Jupyter](.\01_az_generated.ipynb)

3. Streamlit application (via interactive GUI) 
```bash
Streamlit run 01_chatbot.py
```

## II. Chat bot - textual / visual 

**Purpose:** Enable via an Open AI model (gpt-4o) to ask questions about an image (include a Streamlit UI interface). Please note that only gpt-4o has visual analysis abilities.

**Usage:**
1. Command line execution 
```python
python .\02_image_analysis.py
```
2. Streamlit application (via interactive GUI) 
```bash
Streamlit run 02_chat_with_image_analysis.py
```

## III. Chat via xls (Read in Qs / Write As) 

**Purpose:** Read queries from an xlsx with a column that is titled in the header row a "User_Query" and  output an updated xls under temp directory with an additional column with  answer. The utility is provided as a Streamlit application. See under data subdirectory sample xlsx that can be used for test/exploration. 

**Usage:**
```python
Streamlit run 03_chat_with_xlsx.py
```

## IV. Conversation-aware Bot

**Purpose:** Create a conversation aware chatbot using the designated GPT model (e.g., gpt-4-32k) This means that while answering the chatbot will be aware of the previous conversation.

**Usage:**
```python
Streamlit run 04_chat_conversation_aware.py
```

## V.  Chat with a doc (pdf) 
**Purpose:** Ask questions on a specific pdf 

**Usage:**
```python
Streamlit run 05_chat_with_pdf.py
```

## VI. Agentic Flow (get answer from Web or General Knowledge):

**Purpose:** Create a chatbot which leverages agentic flow (based on LangChain framework) and decides whether to use general knowledge or Web Search using the designated GPT model (.g., gpt-4-32k). The sample is  provided as a simple streamlit app

**Usage:**
```python
Streamlit run 06_chat_with_web_search.py
```


## 7. Chat leveraging new knowledge (simple RAG)

**Purpose:** Answer questions while retrieving relevant documents to answer. Leverage the sample documents under data\RAG subfolder

**Usage:**
```python
Streamlit run 07_chat_via_RAG.py
```



