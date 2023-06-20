"""GUI for the document processing app."""
import PyPDF2
import streamlit as st
from dotenv import dotenv_values

from document_processing.extraction.extraction import send_request

img_path = "data/images"
path_pdf = "data/input"
output_path = "data/output"
config = dotenv_values(".env")
# Create a file uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# If a file was uploaded
if uploaded_file is not None:
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    # Save the uploaded file in the "data/input/" folder
    with open("data/input/" + uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Loop through each page and display its contents
    page = pdf_reader.pages[0]
    st.text_area(label="PDF", value=page.extract_text(), height=400)

    # now we generate the prompt
    page = pdf_reader.pages[0]
    page = page.extract_text()

    # now add a field to enter the prompt
    pre_prompt = st.text_input(label="Pre-Prompt", value="")

    # now add a field to enter the post prompt
    post_prompt = st.text_input(label="Post-Prompt", value="")

    # now add a start button to start the extraction
    start_button = st.button(label="Start Extraction")

    # only start the extraction if the button is pressed
    if start_button:
        # generate the prompt
        prompt = pre_prompt + "\n" + page + "\n" + post_prompt

        # send the request to the api
        response = send_request(text=prompt, token=str(config["AA_Token"]))

        # display the response in a text area
        st.text_area(label="Response", value=response)
