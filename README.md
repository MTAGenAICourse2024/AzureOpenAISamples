<div align="center">
<h1> MTA - Practical Applications of Generative AI </h1>
<br>

</div>

## 🚀 Quick Start Guide

Welcome to - Practical Applications of Generative AI Course Repository ! This guide will help you get started with setting up the environment on your local machine. Follow the steps below and then get started leveraging the code samples in this repository. 

### 📋 Prerequisites

- Python (A MUST: version 3.11.9 or higher - [Download Python](https://www.python.org/downloads/) and MAKE SURE to checkbox the `add to PATH` option during installation)
- Git ([Download Git](https://git-scm.com/downloads))

### 🛠️ Onboarding to Azure Open AI 

1. Microsoft offers Azure benefits to students through the Azure for Students program, which provides $100 in free credits.

- Visit Azure for Students and sign up using your academic email (e.g., yourname@mta.ac.il).
- You'll receive $100 in Azure credits without needing a credit card.

2. In order to signup for an Azure subscription, go to the [Azure Portal](https://portal.azure.com/)
- Click "Create a free account" (if you don’t have one).
- Sign in with a Microsoft account and follow the registration steps.
- Choose a subscription type (e.g., "Pay-As-You-Go" if no free credits are available).
- Enter payment details (if required).

3. Create an Azure OpenAI Service Instance

   Once you have an Azure subscription, follow these steps:

   - Navigate to Azure OpenAI:
        Go to the Azure OpenAI Service
        Click "Create" to set up a new OpenAI service.

   - Choose a Subscription & Resource Group:
        Select the Azure subscription (e.g., "Azure for Students" if available).
        Create or choose a Resource Group.

    - Configure Deployment Details:
        Region: Choose an available region (e.g., East US, West Europe).
        Pricing Tier: Choose based on your needs (check if any free tiers are available).
        Quota Application: You might need to apply for access to Azure OpenAI (Microsoft reviews and approves use cases).

    - Review & Deploy:
        Click "Review + Create" and then "Create".
        Once deployed, navigate to the Azure OpenAI Studio to start using models like GPT-

4. Get API Keys & Use the Service

   After setting up Azure OpenAI, you’ll need to get API keys:

    - Go to Azure Portal > OpenAI Resource > Keys and Endpoints.
    - Copy the API Key and Endpoint URL.
    - Use these credentials in your applications (e.g., Python, JavaScript).

5. Testing & Using OpenAI Models

   To interact with OpenAI models:

    Azure OpenAI Studio: OpenAI Studio lets you experiment with models.
    Python Example:

    ```python
   import openai

   openai.api_type = "azure"
   openai.api_base = "https://your-endpoint.openai.azure.com/"
   openai.api_version = "2023-03-15-preview"
   openai.api_key = "your-api-key"

   response = openai.ChatCompletion.create(
      engine="gpt-4",
      messages=[{"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": "Hello, how are you?"}]
   )

   print(response["choices"][0]["message"]["content"])


6. (Optional) Apply for Increased Quota

   If you need more access, submit a quota increase request through Azure OpenAI Service > Quotas.

### 💻 Setting Up Your IDE

#### VS Code

1. Download and install [VS Code](https://code.visualstudio.com/).
2. Install the Python extension for VS Code.
3. Open the project folder in VS Code.

#### PyCharm

1. Download and install [PyCharm](https://www.jetbrains.com/pycharm/).
2. Open the project folder in PyCharm.
3. Go to `File > Settings > Project: Project Name > Project Interpreter` and select the appropriate Python interpreter.

#### GHCP

Follow the instruction on how to install and use GHCP in your IDE 

[VS Code](https://code.visualstudio.com/)
1. Open VS Code.
2. Go to the Extensions Marketplace (Ctrl + Shift + X or Cmd + Shift + X on macOS).
3. Search for "GitHub Copilot".
4. Click Install on the GitHub Copilot extension.
5. (Optional) Also install GitHub Copilot Chat for AI-powered chat assistance.
6. Authenticate GitHub Copilot
   - After installation, open VS Code Settings (Ctrl + ,).
   - Search for Copilot and enable the extension.
   - When prompted, sign in to GitHub.
   - Authorize GitHub Copilot in your browser.
   - Return to VS Code, and it should now be activated.
or [PyCharm]
1.  Open PyCharm.
2. Go to File > Settings (Ctrl + Alt + S or Cmd + , on macOS).
3. Navigate to Plugins.
4. In the Marketplace tab, search for "GitHub Copilot".
5. Click Install and wait for the installation to complete.
6. Restart PyCharm to apply changes.
7. Authenticate GitHub Copilot
   - After restarting, open Settings (Ctrl + Alt + S).
   - Go to Tools > GitHub Copilot.
   - Click Sign in to GitHub.
   - A browser window will open—log in to your GitHub account.
   - Authorize GitHub Copilot.


### ⚙️ Setting Up the Project

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/MTAGenAICourse2024/AzureOpenAISamples.git
   ```
2. Create .env file that should be at your local repository directory 


   ```bash
   ENDPOINT_URL=<YOUR ENDPOINT URL>
   DEPLOYMENT_NAME="gpt-4-32k"
   AZURE_OPENAI_API_KEY=<YOUR API KEY>
   AZURE_OPENAI_LLM_35="gpt-35-turbo"
   AZURE_OPENAI_API_VERSION="2025-01-01-preview"
   AZURE_OPENAI_LLM_4="gpt-4"
   ```

   See below an screenshot that illustrates from where to get the info on the subscription of your enpoint and Azure openai key 
   ![Image](https://github.com/user-attachments/assets/c478e5f8-4e8e-4304-8ff5-e7309a582274)

3. If you download it directly from the Teams channel, make sure to rename to `.env`


