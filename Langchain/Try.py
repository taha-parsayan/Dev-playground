import os
import sys
from langchain_community import document_loaders
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



# Add the parent directory to the system path
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)
from Update_Git import git_add, git_commit, git_push



# Update Git Repository
try:
    file_path = os.path.join(current_path, "Try.py")
    git_add(file_path)
    git_commit("Update Try.py")
    git_push("main")
except Exception as e:
    print(f"An error occurred while updating the git repository\n: {e}")



# Get the document from webpage and split it into chunks
def document_loader(url):

    # Load documents from a given URL
    loader = WebBaseLoader(url)
    docs = loader.load()

    # Split the documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
    )

    split_docs = splitter.split_documents(docs)

    return split_docs

def create_db(docs):
    pass

def create_chain():
    pass


# Main
if __name__ == "__main__":
    print("\n")
    url = "https://github.com/taha-parsayan/OPETIA"
    docs = document_loader(url)
    print(f"Number of documents loaded: {docs}")

