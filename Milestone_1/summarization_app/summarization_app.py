import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

# Load environment variables
load_dotenv()

# Initialize Groq API client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  # Ensure this is defined in your .env file
)

# Function to summarize text using Groq API
def summarize_text_groq(input_text, model="llama-3.3-70b-versatile", max_tokens=150):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{input_text}",
                },
            ],
            model=model,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"API call failed: {e}")

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_pdf):
    try:
        pdf_reader = PdfReader(uploaded_pdf)
        if pdf_reader.is_encrypted:
            st.error("❌ The uploaded PDF is encrypted and cannot be processed.")
            return ""
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""  # Handle pages with no text gracefully
        if not text.strip():
            raise RuntimeError("No extractable text found in the PDF.")
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")

# Function to save summary as a PDF
def save_summary_to_pdf(summary_text):
    try:
        # Use BytesIO to create an in-memory PDF
        summary_stream = BytesIO()
        c = canvas.Canvas(summary_stream, pagesize=letter)
        c.drawString(100, 750, "Summary:")
        text_object = c.beginText(100, 730)  # Start the text object at this position
        text_object.setFont("Helvetica", 10)
        
        # Split text into lines for better formatting
        lines = summary_text.splitlines()
        for line in lines:
            text_object.textLine(line)
        
        c.drawText(text_object)
        c.save()

        # Seek to the start of the BytesIO stream
        summary_stream.seek(0)
        return summary_stream
    except Exception as e:
        raise RuntimeError(f"Failed to save summary to PDF: {e}")

# Streamlit App Setup
st.set_page_config(page_title="Text Summarization App", page_icon="📚", layout="wide")
st.title("📚 Text Summarization App with Groq API")

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f4f7fc;
        padding: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px 32px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        margin-top: 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# Instructions or greeting
st.markdown("""
    <div style="font-size: 18px; color: #444;">
    Welcome to the Text Summarization App! You can enter text or upload a PDF to get a concise summary using Groq API. Feel free to explore the tabs below.
    </div>
    """, unsafe_allow_html=True)

# Tabs for manual text and PDF upload
tab1, tab2, tab3 = st.tabs(["Manual Text Input", "PDF Upload", "🗣️ Chat with Bot"])

# Manual Text Input Tab
with tab1:
    st.subheader("📝 Enter Your Text")
    input_text = st.text_area("Enter the text to summarize", height=200, max_chars=2000)
    if st.button("🔍 Summarize Text"):
        if input_text:
            with st.spinner("Summarizing your text..."):
                try:
                    summary = summarize_text_groq(input_text)
                    st.success("✅ Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
        else:
            st.warning("⚠️ Please enter some text to summarize!")

# PDF Upload Tab
with tab2:
    st.subheader("📤 Upload a PDF for Summarization")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf is not None:
        with st.spinner("Extracting text from PDF..."):
            try:
                extracted_text = extract_text_from_pdf(uploaded_pdf)
                st.success("✅ Text extracted from PDF.")
                st.text_area("📄 Extracted Text:", extracted_text, height=200)
                
                if st.button("🔍 Summarize PDF"):
                    with st.spinner("Summarizing the extracted text..."):
                        try:
                            summary = summarize_text_groq(extracted_text)
                            st.success("✅ PDF Summary:")
                            st.write(summary)

                            # Save the summary to a new PDF
                            summary_pdf = save_summary_to_pdf(summary)
                            st.download_button(
                                label="💾 Download Summary PDF",
                                data=summary_pdf,
                                file_name="summary.pdf",
                                mime="application/pdf",
                            )
                        except Exception as e:
                            st.error(f"❌ An error occurred: {e}")
            except RuntimeError as e:
                st.error(f"❌ {e}")

# Chat with Bot Tab
with tab3:
    st.subheader("🗣️ Chat with the Bot")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"**User**: {message['content']}")
        else:
            st.write(f"**Bot**: {message['content']}")

    user_input = st.text_input("Type your message:", "")

    if st.button("Send Message"):
        if user_input:
            # Add user input to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Get bot's response
            with st.spinner("Bot is typing..."):
                try:
                    response = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.3-70b-versatile",  # Groq model
                    )
                    bot_message = response.choices[0].message.content.strip()

                    # Add bot response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": bot_message})

                    st.write(f"**Bot**: {bot_message}")
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
        else:
            st.warning("⚠️ Please enter a message to send.")
