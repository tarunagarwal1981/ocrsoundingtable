import streamlit as st
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

# Streamlit app
st.title("PDF OCR Extractor")
st.write("Upload a PDF file, and this app will extract text using OCR.")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("PDF uploaded successfully!")

    # Convert PDF to images
    st.write("Converting PDF to images...")
    pages = convert_from_path("uploaded_file.pdf", dpi=300)
    st.write(f"Total pages: {len(pages)}")

    # OCR on each page
    extracted_text = ""
    for i, page in enumerate(pages):
        st.write(f"Processing page {i + 1}...")
        # Convert page to image
        page_image = page.convert("RGB")

        # Perform OCR
        text = pytesseract.image_to_string(page_image)
        extracted_text += f"--- Page {i + 1} ---\n{text}\n"

        # Display the page image
        st.image(page_image, caption=f"Page {i + 1}", use_column_width=True)

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

    # Clean up temporary file
    os.remove("uploaded_file.pdf")
