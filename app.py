import streamlit as st
import pdfplumber
import pandas as pd
from pdfplumber.utils import extract_text, get_bbox_overlap, obj_to_bbox
from PIL import Image
import pytesseract
import io
import base64
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(text):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text:\n\n{text}"
                }
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"

def process_pdf(pdf_file):
    all_text = []
    tables = []
    images = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            filtered_page = page
            chars = filtered_page.chars
            page_tables = page.find_tables()
            
            for table in page_tables:
                first_table_char = page.crop(table.bbox).chars[0]
                filtered_page = filtered_page.filter(lambda obj: get_bbox_overlap(obj_to_bbox(obj), table.bbox) is None)
                chars = filtered_page.chars
                df = pd.DataFrame(table.extract())
                df.columns = df.iloc[0]
                markdown = df.drop(0).to_markdown(index=False)
                chars.append(first_table_char | {"text": markdown})
                tables.append(df)
            
            page_text = extract_text(chars, layout=True)
            all_text.append(page_text)
            
            for image in page.images:
                images.append({
                    "page_number": page.page_number,
                    "data": image["stream"].get_data()
                })

    return "\n".join(all_text), tables, images

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

st.set_page_config(layout="centered", page_title="Advanced PDF & Image Extractor with Summarization")

st.title("Advanced PDF & Image Extractor with Summarization")

st.markdown("""
<style>
.stApp {
    max-width: 800px;
    margin: 0 auto;
}
.stButton > button {
    width: 100%;
}
.stDataFrame {
    max-height: 300px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        with st.spinner("Extracting content from PDF..."):
            text, tables, images = process_pdf(uploaded_file)
        
        st.subheader("Extracted Text")
        st.text_area("", value=text, height=200)
        
        with st.spinner("Generating summary..."):
            summary = summarize_text(text)
        
        st.subheader("Text Summary")
        st.text_area("", value=summary, height=150)
        
        st.subheader("Extracted Tables")
        for i, table in enumerate(tables):
            st.write(f"Table {i+1}")
            st.dataframe(table)
        
        st.subheader("Extracted Images")
        for i, image in enumerate(images):
            st.image(image["data"], caption=f"Image from page {image['page_number']}")
            
            # Provide download link for each image
            b64 = base64.b64encode(image["data"]).decode()
            href = f'<a href="data:image/png;base64,{b64}" download="image_page_{image["page_number"]}.png">Download Image</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        # Provide download links for extracted text and summary
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Extracted Text",
                data=text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        with col2:
            st.download_button(
                label="Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )
    else:
        with st.spinner("Extracting text from Image..."):
            text = extract_text_from_image(uploaded_file)
        
        st.subheader("Extracted Text")
        st.text_area("", value=text, height=200)
        
        with st.spinner("Generating summary..."):
            summary = summarize_text(text)
        
        st.subheader("Text Summary")
        st.text_area("", value=summary, height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Extracted Text",
                data=text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        with col2:
            st.download_button(
                label="Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )
else:
    st.info("Please upload a PDF or Image file to extract content and generate a summary.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, pdfplumber, and Groq API")
