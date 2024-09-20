# streamlit run /Users/physics_jordan/Data_Science/Personal_Project/document_qa_modules/main.py

from pinecone import Pinecone, ServerlessSpec
import os
import shutil
# import docx
import pdfplumber
import data_files_manager as dfm
import streamlit_launcher as stl
import chunk_embed as cbed
# Load the Hugging Face model and tokenizer
# Load model directly
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
# Use a pipeline as a high-level helper
from transformers import pipeline

# Step1: Launch streamlit page
launcher = stl.Streamlit()


# Step2: Launching sidebar for uploading files using
# Streamlit object created in Step1 and get uploaded files.
files = launcher.sidebar()

# Step3: Before working on uploaded files, we first build the architechture for holding the data in the files.
if files:
    # Creating an object for ManageData Class in data_files_manager.py
    data_manager = dfm.ManageData(files)

    # Moving existing files in default folder to different folder,
    # extract data from doc, create chunks and embeddings
    data_manager.move_files(src_directory = 'uploads', dest_directory = 'previous_uploaded_files')

    #  Save uploaded files to custom directory
    number_of_files = data_manager.upload_file_save()
    for file in os.listdir('uploads'):
        # Process the uploaded files to extract data from it
        document_text, document_name = data_manager.process_uploaded_doc(file_dir='uploads', document_text='', document_name=file)
        # print("Document text: ", document_text)

        # Create an object for class ChunkEmbed
        chunker_embedder = cbed.ChunkEmbed()
        # Creating chunks from large data in document_text
        text_chunks = chunker_embedder.chunker(document_text)
        print("Text _chunks: ", text_chunks)
        embeddings = chunker_embedder.create_pine_embeddings(text_chunks, document_name=document_name)

else:
    launcher.upload_warning()
# Step4: Initialize the pipeline for question and answer RAG model from hugging face
tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

launcher.question_answer(nlp)
# data_manager.move_files(src_directory, dest_directory)
