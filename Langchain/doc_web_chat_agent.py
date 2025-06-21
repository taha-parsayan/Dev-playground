"""
Interactive Chat Agent with Document Retrieval and Web Search using LangChain

This script implements a conversational agent that answers user questions using both:
1. A vector-based retriever for contextual documents (e.g., FreeSurfer, OPETIA), and
2. A web search tool (Tavily) for up-to-date information not covered in the documents.

Key features:
- Loads and chunks web content using LangChain's WebBaseLoader
- Builds a FAISS vector store with OpenAI embeddings
- Creates an OpenAI functions-enabled agent that can choose between document retrieval and web search tools
- Maintains chat history for multi-turn conversations
- Automatically updates the script via Git with `Update_Git.py`
- Designed to handle biomedical tools like FreeSurfer and OPETIA

To use:
- Run the script and type a question (e.g., "What is OPETIA?")
- Type "exit" to stop the session

Requirements:
- LangChain, FAISS, OpenAI, Tavily, python-dotenv
- A `.env` file with necessary API keys (e.g., OpenAI, Tavily)

Author: Mohammadtaha Parsayan
"""


import os
import sys
from dotenv import load_dotenv
from langchain_functions import *

# Add the parent directory to the system path
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)
from Update_Git import git_add, git_commit, git_push


# Load environment variables
load_dotenv(os.path.join(current_path, ".env"))

# Update Git Repository
try:
    file_path = os.path.join(current_path, "doc_web_chat_agent.py")
    git_add(file_path)
    git_commit("Updated doc_web_chat_agent.py")
    git_push("main")
except Exception as e:
    print(f"An error occurred while updating the git repository\n: {e}")



# Main
if __name__ == "__main__":
    print("\n_______________________")
    docs = document_loader("https://en.wikipedia.org/wiki/FreeSurfer")
    vector_store = create_db(docs)
    chain = create_chain(vector_store)

    chat_history = []

    while True:
        user_input = input("You:\n")
        if user_input.lower() == "exit":
            break
        response = process_chat(chain, user_input, chat_history, docs)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))
        print("AI:\n", response)
        print("\n")
        