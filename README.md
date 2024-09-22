# document_qa_modules
 Project: Question answer from a uploaded document using streamlit for user interface, pinecone for generating embeddings and deepset-roberta-base-squad2 model for dealing with user question and generate answer the question.


 For installing dependencies, I recommend to create/open virtual environment locally on your desktop. Then follow steps below.

 1. Clone the repository:
    <https://github.com/Jordan-Karangala/QA_deepset-roberta-base-squad2.git>
 2. cd to the peoject location.
 3. Installation: Use requirements.txt file to install all the dependencies for this project.
 4. Once the installation is done, check the files whether chunk_embed.py, data_files_manager.py, streamlit_launcher.py are present in the folder where cloning s done.
 5. Remove any files in the folders: previous_uploaded_files and uploads

Code is ready to use if you have already created an account with streamlit and pinecone.

If Not: 
PINECONE Setup:

Install Pinecone
Ready to get started with Pinecone? First, install the Python SDK:
pip install pinecone

Go to: <https://www.pinecone.io/> and signup.
You will have a default API key generated by pinecone which can be used later in the project or you can create a new api by clicking on create API Key.

After setting up with api key, go to database/indexes. There you can create a index


 Testing/Running the model:
 If you want to use your terminal for initiating the app, use the following command in your terminal.
 <# streamlit run path/to/your/main.py #>

If you want to run from PyCharm IDE, follow the steps bellow.

 

