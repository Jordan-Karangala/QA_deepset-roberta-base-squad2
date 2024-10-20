# streamlit run /Users/physics_jordan/Data_Science/Personal_Project/document_qa_modules/main.py

from pinecone import Pinecone, ServerlessSpec
import os
import shutil
# import docx
import pdfplumber
import data_files_manager as dfm
import streamlit_launcher as stl
import chunk_embed

pc = chunk_embed.pc
index_name = chunk_embed.index_name
index = pc.Index('multilingual-e5-large')# Your free to use anyother embeddings models, multilingual-e5-large is used in this project

# Load the Hugging Face model and tokenizer
# Load model directly
import streamlit as st
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
# Use a pipeline as a high-level helper
from transformers import pipeline

# Welcome page
st.title('Hello Streamlit!')
st.write("This is a simple 'Q&A' Streamlit app.")
# Initializing a session state variable 'count'
if 'count' not in st.session_state:
    st.session_state.count = 0



# To return back to home ppage
if st.session_state.count >= 1:
    st.button("Home")

if 'upload' not in st.session_state:
    st.session_state.upload = False
def click_button_to_upload():
    st.session_state.upload = True
    # # Welcome page
    # st.title('Hello Streamlit!')
    # st.write("This is a simple 'Q&A' Streamlit app.")

def generate_answer(query):
    input_query = query
    x = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[input_query],
        parameters={
            "input_type": "query"
        }
    )

    results = index.query(
        namespace="ns1",
        vector=x[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True
    )

    # print(results['matches'][0])
    # print(results['matches'][1]['metadata']['text'])
    content = ""
    for text in results['matches']:
        content += text['metadata']['text']
    print(content)
    return content
def question_answer():
    # Step4: Initialize the pipeline for question and answer RAG model from hugging face
    tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

    user_question = st.text_input("Enter your question about the PDF content:")
    if st.button("Generate Answer"):

        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:
            st.info("Processing PDF files and generating answer... (this might take a moment)")
            input_query = user_question
            content = generate_answer(input_query)
            print(content[:100])
            QA_input = {
                'question': input_query,
                'context': content
            }
            answer = nlp(QA_input)  # Call preprocess_function from preprocess.py
            print(answer)
            st.info("Processing complete!")
            st.write("Answer:")
            st.write(answer)
    # data_manager.move_files(src_directory, dest_directory)
# Step2: Launching sidebar for uploading files using
if st.session_state.upload:
    st.sidebar.title("Upload PDF Files")
    uploaded_files = st.sidebar.file_uploader("Choose PDF files", accept_multiple_files=True,
                                              type=["pdf", "csv", "txt", 'docx'])



# Streamlit object created in Step1 and get uploaded files.
#     files = st.sidebar()

    # Step3: Before working on uploaded files, we first build the architechture for holding the data in the files.
    if uploaded_files:


        # Creating an object for ManageData Class in data_files_manager.py
        data_manager = dfm.ManageData(uploaded_files)

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
            chunker_embedder = chunk_embed.ChunkEmbed()
            # Creating chunks from large data in document_text
            text_chunks = chunker_embedder.chunker(document_text)
            print("Text _chunks: ", text_chunks)
            embeddings = chunker_embedder.create_pine_embeddings(text_chunks, document_name=document_name)
        question_answer()
        # st.text_input("Enter your question about the PDF content:", on_change="")
    else:
        # launcher.upload_warning()
        st.warning("Please upload files before proceeding.")

if not st.session_state.upload:

    if st.button("Upload files", on_click=click_button_to_upload):
        st.session_state.count += 1





