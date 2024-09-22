# document_qa_modules
 Project: Question answer from a uploaded document using streamlit for user interface, pinecone for generating embeddings and deepset-roberta-base-squad2 model for dealing with user question and generate answer the question.

Just to quick check on app, you can use docker if you have an account:
Run this code in your terminal<docker pull your_dockerhub_username/document_qa>

Or
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
Get started with Pinecone. First, install the Python SDK:
pip install pinecone


Go to: <https://www.pinecone.io/> and signup.
You will have a default API key generated by pinecone which can be used later in the project or you can create a new api by clicking on create API Key.


In the project folder, open chunk_embed.py file and look for lines below to eneter your api key.
<pc = Pinecone(api_key="Enter/your/api/key/here")>. save and close the file.

check if streamlit is installed or not:
If not:
pip install streamlit

Your are all set to go now.

 Testing/Running the model:
 If you want to use your terminal for initiating the app, use the following command in your terminal.
 <# streamlit run path/to/your/main.py #>

If you want to run from PyCharm IDE, follow the steps bellow.
Open your Streamlit app file (e.g., app.py) in PyCharm.
Edit the app to run using Python code: Replace the usual terminal-based streamlit run command with this in your code:
import os

if __name__ == "__main__":
    os.system("streamlit run your_app.py")
Configure PyCharm Run Settings:
In PyCharm, go to Run > Edit Configurations.
Click on the "+" icon to add a new configuration and choose Python.
Name it (e.g., Streamlit).
Set the Script path to your your_app.py file.
Set the Python interpreter to your desired environment (ensure Streamlit is installed there).
Click Apply and OK.
Now, you can run your Streamlit app using the PyCharm run button.

 

