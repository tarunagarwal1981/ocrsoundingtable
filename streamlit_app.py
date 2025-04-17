import streamlit as st
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
import sys

# Streamlit app
st.title("PDF OCR Extractor")
st.write("Upload a PDF file, and this app will extract text using OCR.")

# Check for dependencies
try:
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("uploaded_file.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write("PDF uploaded successfully!")
        
        try:
            # Convert PDF to images
            with st.spinner("Converting PDF to images..."):
                pages = convert_from_path("uploaded_file.pdf", dpi=300)
            st.write(f"Total pages: {len(pages)}")
            
            # OCR on each page
            extracted_text = ""
            progress_bar = st.progress(0)
            
            for i, page in enumerate(pages):
                status_text = st.empty()
                status_text.write(f"Processing page {i + 1} of {len(pages)}...")
                
                # Convert page to image
                page_image = page.convert("RGB")
                
                # Perform OCR
                text = pytesseract.image_to_string(page_image)
                extracted_text += f"--- Page {i + 1} ---\n{text}\n"
                
                # Display the page image
                st.image(page_image, caption=f"Page {i + 1}", use_column_width=True)
                
                # Update progress
                progress_bar.progress((i + 1) / len(pages))
                
            progress_bar.empty()
            
            # Display extracted text
            st.write("### Extracted Text")
            st.text_area("OCR Output", extracted_text, height=300)
            
            # Option to download the extracted text
            st.download_button(
                label="Download Extracted Text",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists("uploaded_file.pdf"):
                os.remove("uploaded_file.pdf")
                
except ImportError as e:
    if "pdf2image" in str(e) or "pytesseract" in str(e):
        st.error("Missing required Python packages. Please install pdf2image and pytesseract.")
    else:
        st.error(f"Import error: {str(e)}")
        
except Exception as e:
    if "poppler" in str(e).lower() or "PDFInfoNotInstalledError" in str(e):
        st.error("Missing Poppler utilities. Make sure poppler-utils is installed on your system.")
        st.info("If you're using Streamlit Cloud, please add a packages.txt file with 'poppler-utils' listed.")
    elif "tesseract" in str(e).lower():
        st.error("Missing Tesseract OCR. Make sure tesseract-ocr is installed on your system.")
        st.info("If you're using Streamlit Cloud, please add a packages.txt file with 'tesseract-ocr' listed.")
    else:
        st.error(f"An error occurred: {str(e)}")
