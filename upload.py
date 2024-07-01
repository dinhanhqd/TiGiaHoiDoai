import streamlit as st
import fitz  # PyMuPDF
from docx import Document
import os
from prepare_vector_db import create_db_from_files  # Import the function

# Create the data directory if it doesn't exist
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def save_uploaded_file(uploaded_file, directory):
    with open(os.path.join(directory, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join(directory, uploaded_file.name)


def read_pdf(file_path):
    document = fitz.open(file_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


def read_word(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def display_files(directory):
    files = os.listdir(directory)
    if "visible_files" not in st.session_state:
        st.session_state.visible_files = {}

    for file in files:
        file_path = os.path.join(directory, file)
        col1, col2 = st.columns([5, 1])

        with col1:
            if st.button(file, key=file):
                if file not in st.session_state.visible_files:
                    st.session_state.visible_files[file] = True
                else:
                    st.session_state.visible_files[file] = not st.session_state.visible_files[file]

        with col2:
            if st.button("Delete", key="delete_" + file):
                os.remove(file_path)
                st.session_state.visible_files.pop(file, None)  # Remove from visible files state
                st.experimental_rerun()  # Refresh the page to reflect the changes

        if file in st.session_state.visible_files and st.session_state.visible_files[file]:
            if file.endswith(".pdf"):
                st.write(read_pdf(file_path))
            elif file.endswith(".docx") or file.endswith(".doc"):
                st.write(read_word(file_path))
        st.write("---")


def main():
    st.title("File Upload")
    # Add "Chunk" button below the file display area
    if st.button("Chunk"):
        with st.spinner("Processing..."):
            create_db_from_files()
        st.success("Vector database updated successfully!")
    # Sidebar for file upload
    st.sidebar.title("File Upload")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF or Word file", type=["pdf", "docx", "doc"])
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file, data_dir)
        st.sidebar.write(f"Uploaded file saved to {file_path}")

    st.write("Files in the data directory:")
    display_files(data_dir)




if __name__ == "__main__":
    main()
