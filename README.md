# Extractor-with-Summarization
# Advanced PDF & Image Extractor with Summarization

## Description
This Streamlit application provides a powerful tool for extracting and analyzing content from PDF files and images. It offers features such as text extraction, table detection, image extraction, and text summarization using the Groq API with the LLaMA3 model.

## Features
- PDF text extraction with layout preservation
- Table detection and extraction from PDFs
- Image extraction from PDFs
- Text extraction from images (PNG, JPG, JPEG)
- Text summarization using Groq API (LLaMA3 model)
- User-friendly interface built with Streamlit

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/RkanGen/Extractor-with-Summarization.git
   cd Extractor-with-Summarization
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install streamlit pdfplumber pytesseract pillow pandas groq python-dotenv
   ```

4. Install Tesseract OCR:
   - On Ubuntu: `sudo apt-get install tesseract-ocr`
   - On macOS: `brew install tesseract`
   - On Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

5. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Use the file uploader to select a PDF or image file

4. The app will extract text, tables, and images (if applicable) and display them

5. A summary of the extracted text will be generated using the Groq API

6. You can download the extracted text, summary, and images using the provided buttons

## Configuration

You can modify the `app.py` file to customize various aspects of the application, such as:
- Changing the Groq API model
- Adjusting the summarization parameters
- Modifying the layout and styling of the Streamlit app

## Troubleshooting

If you encounter any issues:
1. Ensure all dependencies are correctly installed
2. Check that your Groq API key is correctly set in the `.env` file
3. Verify that Tesseract OCR is properly installed and accessible in your system PATH

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web app framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF parsing
- [Groq](https://groq.com/) for the AI-powered summarization
- [pytesseract](https://github.com/madmaze/pytesseract) for OCR capabilities
