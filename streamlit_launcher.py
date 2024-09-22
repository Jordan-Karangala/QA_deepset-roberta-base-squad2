import streamlit as st
import chunk_embed
pc = chunk_embed.pc
index_name = chunk_embed.index_name
index = pc.Index('multilingual-e5-large')# Your free to use anyother embeddings models, multilingual-e5-large is used in this project 

class Streamlit:
    def __init__(self):
        # st.set_page_config(page_title="Question Answerer using RAG", layout="wide")
        st.title('Hello Streamlit!')
        st.write('This is a simple Streamlit app.')
        # Sidebar for file upload
        st.sidebar.title("Upload PDF Files")
        st.write("Upload PDF files on the sidebar to analyze them.")
        return


    def sidebar(self):
        uploaded_files = st.sidebar.file_uploader("Choose PDF files", accept_multiple_files=True,
                                                  type=["pdf", "csv", "txt", 'docx'])
        return uploaded_files

    # def upload_success_msg(self):
    #     st.sidebar.success(f"File '{uploaded_file.name}' saved successfully to '{UPLOAD_DIR}'!")

    def generate_answer(self, query):
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
        # print(text['metadata']['text'])


    def question_answer(self, nlp):
        # User input for question
        user_question = st.text_input("Enter your question about the PDF content:")
        if st.button("Generate Answer"):

            if user_question.strip() == "":
                st.warning("Please enter a question.")
            else:
                st.info("Processing PDF files and generating answer... (this might take a moment)")
                input_query = user_question
                content = self.generate_answer(input_query)
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


    def upload_warning(self):
        st.warning("Please upload files before proceeding.")
