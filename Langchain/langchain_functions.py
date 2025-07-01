"""
This module provides a function to create a LangChain function that can be used to call an LLM.

This module implements a conversational agent that answers user questions using both:
1. A vector-based retriever for contextual documents (e.g., FreeSurfer, OPETIA), and
2. A web search tool (Tavily) for up-to-date information not covered in the documents.
3. Save chat history in a SQLite database and load it on startup.

Key features:
- Loads and chunks web content using LangChain's WebBaseLoader
- Builds a FAISS vector store with OpenAI embeddings
- Creates an OpenAI functions-enabled agent that can choose between document retrieval and web search tools
- Maintains chat history for multi-turn conversations
- Automatically updates the script via Git with `Update_Git.py`
- Designed to handle biomedical tools like FreeSurfer and OPETIA

Requirements:
- LangChain, FAISS, OpenAI, Tavily, python-dotenv
- A `.env` file with necessary API keys (e.g., OpenAI, Tavily)

Author: Mohammadtaha Parsayan
"""

#----------------------------------------------------------------------------
# Import libraries
#----------------------------------------------------------------------------

import os
import sys
from langchain_community import document_loaders
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools.retriever import create_retriever_tool
from langchain_tavily import TavilySearch
from langchain.agents import AgentExecutor, create_openai_functions_agent
import sqlite3
from datetime import datetime

#----------------------------------------------------------------------------
# SQLite database setup
#----------------------------------------------------------------------------

# SQLite load chat history from database
def load_chat_history_from_database():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    # Always try to create the table (harmless if it already exists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Now read chat history
    cursor.execute("SELECT role, message FROM history ORDER BY id ASC")
    rows = cursor.fetchall()
    history = []
    for role, msg in rows:
        if role == "human":
            history.append(HumanMessage(content=msg))
        else:
            history.append(AIMessage(content=msg))

    conn.close()  # optional but good practice
    return history


# Save chat history in the database
def save_message_in_database(role, message):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO history (role, message, timestamp) VALUES (?, ?, ?)",
                   (role, message, timestamp))
    conn.commit()

#----------------------------------------------------------------------------
# Langchain functions
#----------------------------------------------------------------------------
'''
1. load the document (webpage or PDF)
2. split the document into chunks
3. create a vector store from the chunks (embeddings)
4. create a chain that uses the vector store and web search tool
5. process the chat with the chain
'''

# Get the document from webpage or PDF and split it into chunks
def document_loader(source_type, path):

    # Load documents
    if source_type == "web":
        loader = WebBaseLoader(path)
        docs = loader.load()
    elif source_type == "pdf":
        loader = PDFPlumberLoader(path)
        docs = loader.load()
    else:
        raise ValueError("Unsupported source type. Use 'web' or 'pdf'.")

    # Split the documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
    )

    split_docs = splitter.split_documents(docs)

    return split_docs

# Create a vector store from the documents
# This will create a FAISS vector store using OpenAI embeddings
def create_db(docs):
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding = embedding)

    return vectorstore

# Create a chain that uses the vector store and web search tool
def create_chain(vector_store):

    # llm model
    model = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 1.5,
    )

    #prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's question based on the given context: {context}. If you cannot find the answer, use the web search tool (Tavily)."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name = "agent_scratchpad")
    ])

    # Parser
    # output_parser = StrOutputParser()

    # Chain
    # chain = create_stuff_documents_chain(
    #     llm = model,
    #     prompt = prompt,
    #     output_parser= output_parser
    # )
    

    '''
    AGENTS:
    1. document from specific webpage (url)
    2. web search tool (Tavily)
    '''

    # 1. tool for document
    retriever = vector_store.as_retriever(search_kwaargs = {"k": 5})  # Convert vector store into a retriever
    retriever_tool = create_retriever_tool(
    retriever,
    "toolbox_search", # identifier for the tool
    "Use this tool when searching for information about FreeSurfer" # description of the tool
    )

    # 2. tool for web search
    search = TavilySearch(
        max_results=5,
        topic="general",
        # include_answer=False,
        # include_raw_content=False,
        # include_images=False,
        # include_image_descriptions=False,
        # search_depth="basic",
        # time_range="day",
        # include_domains=None,
        # exclude_domains=None,
        # country=None
    )

    # List of tools - we have 2 tools here
    tools = [search, retriever_tool]

    # Create an agent that uses the LLM, prompt, and tools (no chain here)
    agent = create_openai_functions_agent(
        llm = model,
        prompt = prompt,
        tools = tools,
    )

    agentExecutor = AgentExecutor(
        agent = agent,
        tools = tools
    )

    return agentExecutor  # Return the retrieval chain


# Function to ask a question
def process_chat(agentExecutor, question, history, docs):
    response = agentExecutor.invoke({
        "input": question,
        "chat_history": history,
        "context": docs
    })

    return response["output"]



"""
How to use this module:

# Main
if __name__ == "__main__":
    print("\n_______________________")
    docs = document_loader("https://en.wikipedia.org/wiki/FreeSurfer")
    vector_store = create_db(docs)
    chain = create_chain(vector_store)

    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = process_chat(chain, user_input, chat_history)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))
        print("AI: ", response)
        print("\n")
"""