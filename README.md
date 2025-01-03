# 📚 Text Summarization App with Groq API 

Welcome to the **📚 Text Summarization App**! This app leverages the **Groq API** for generating summaries of text from various inputs, including manual text entry and PDF uploads. Additionally, it includes a chatbot feature to interact with the app and get real-time responses.

## Features
- **Manual Text Input**: Paste or type any text, and the app will summarize it using the Groq API.
- **PDF Upload**: Upload a PDF file, and the app will extract the text and summarize it. You can also download the summarized content as a new PDF.
- **Chat with Bot**: Engage in a chat with a helpful assistant to answer questions or provide summaries of any input.

## Technologies Used
- **Streamlit**: For building the web interface.
- **Groq API**: For natural language processing and text summarization.
- **PyPDF2**: For extracting text from PDF files.
- **ReportLab**: For generating PDF summaries.
- **Pillow**: For image handling (if required).
- **Python-dotenv**: For loading environment variables securely.

## Setup Instructions

### Prerequisites
Ensure that you have Python 3.7+ installed.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/text-summarization-app.git
cd text-summarization-app
```
### 2. Install Dependencies
Create a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
### 3. Configure Environment Variables
Create a .env file in the root of the project with the following content:
```bash
makefile
GROQ_API_KEY=your_groq_api_key_here
Make sure to replace your_groq_api_key_here with your actual API key from Groq.
```
### 4. Run the App
Once the dependencies are installed and the environment is configured, run the app with Streamlit:
```bash
Copy code
streamlit run app.py
```
This will start the app, and you can access it in your browser at http://localhost:8501.

# App Overview
### Manual Text Input Tab
In this section, you can enter text into the text area, and the app will summarize it using the Groq API. The summary will be displayed after processing.

# PDF Upload Tab
You can upload a PDF file, and the app will extract its text. Once extracted, you can summarize the text and download the resulting summary as a new PDF file.

# Chat with Bot Tab
This feature allows you to interact with a chatbot assistant. You can ask the bot to summarize text, answer questions, or assist with any other queries. It stores the conversation history and shows both user and bot messages.

# Contributing
We welcome contributions! If you'd like to contribute to this project, feel free to:

# Fork the repository.
- Create a feature branch (git checkout -b feature-name).
- Commit your changes (git commit -am 'Add new feature').
- Push to the branch (git push origin feature-name).
- Open a pull request.
# Acknowledgments
- Groq API for providing powerful language models for text summarization.
- Streamlit for creating an easy-to-use platform for building interactive web apps.
- PyPDF2 and ReportLab for handling PDF processing.

# Enjoy using the 📚 Text Summarization App! 😊
### Notes:
1. The `requirements.txt` should include the dependencies you used in the project (e.g., `streamlit`, `groq`, `PyPDF2`, `reportlab`, `python-dotenv`, etc.).

Let me know if you need any more details!
