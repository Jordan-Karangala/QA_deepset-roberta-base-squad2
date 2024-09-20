import os
import shutil
# import docx
import pdfplumber
import streamlit as st

class ManageData:
    def __init__(self, uploaded_files):
        self.uploaded_files = uploaded_files


    # 1. Function to extract text from PDF
    def extract_text_from_pdf(self,file_path):
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text

    # # 2. Function to extract text from Word document
    # def extract_text_from_docx(self,file_path):
    #     doc = docx.Document(file_path)
    #     return "\n".join([para.text for para in doc.paragraphs])

    # 3. Function to extract text from a TXT file
    def extract_text_from_txt(self,file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def move_files(self, src_directory, dest_directory):
        # Ensure the destination directory exists
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        # List all files in the source directory
        for file_name in os.listdir(src_directory):
            src_file = os.path.join(src_directory, file_name)
            dest_file = os.path.join(dest_directory, file_name)

            # Check if the source file exists before moving
            if os.path.exists(src_file):
                try:
                    shutil.move(src_file, dest_file)
                    print(f"Moved: {src_file} -> {dest_file}")
                except Exception as e:
                    print(f"Failed to move {src_file} due to: {e}")
            else:
                print(f"Source file does not exist: {src_file}")


    def upload_file_save(self):
        number_of_files = 0
        file_dir = 'uploads'
        document_text = ""
        # if self.uploaded_files:
        for uploaded_file in self.uploaded_files:
            # Save each uploaded file to the upload directory
            save_path = os.path.join(file_dir, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            number_of_files += 1
        return number_of_files
            # st.sidebar.success(f"File '{uploaded_file.name}' saved successfully to '{UPLOAD_DIR}'!")
            #
            # # Extract data from document
            # data = self.process_uploaded_doc(file_dir, document_text)
            # #  Once data extracted
            # if data:  # Check if there's data to create embeddings
            #     self.create_embeddings(data=data, document_name=uploaded_file.name)
            # else:
            #     st.warning("No content found in the uploaded files."))


    def process_uploaded_doc(self, file_dir, document_text, document_name):
        # for file_name in os.listdir(file_dir):
        # Check if it's a file
        if os.path.isfile(os.path.join(file_dir, document_name)):
            print(document_name)
            file_type = document_name.split('.')[-1].lower()
            file_path = os.path.join(file_dir, document_name)
            if file_type == 'pdf':
                document_text = self.extract_text_from_pdf(file_path)
                document_name = document_name
            # elif file_type == 'docx':
            #     document_text = self.extract_text_from_docx(file_path)
            elif file_type == 'txt':
                document_text = self.extract_text_from_txt(file_path)
                document_name = document_name
            return document_text, document_name
        else:
            print("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")






