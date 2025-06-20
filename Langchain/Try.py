import os
import sys
from dotenv import load_dotenv
from langchain_community import document_loaders
from langchain_community.document_loaders import WebBaseLoader
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
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent


# Add the parent directory to the system path
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)
from Update_Git import git_add, git_commit, git_push


# Load environment variables
load_dotenv(os.path.join(current_path, ".env"))

# Update Git Repository
try:
    file_path = os.path.join(current_path, "Try.py")
    git_add(file_path)
    git_commit("Updated Try.py")
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
        chunk_size = 100,
        chunk_overlap = 20,
    )

    split_docs = splitter.split_documents(docs)

    return split_docs


def create_db(docs):
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding = embedding)

    return vectorstore


def create_chain(vector_store):

    # llm model
    model = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,
    )

    #prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's question based on the given context: {context} and try to be as annoying as possible."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name = "agent_scratchpad")
    ])

    # Parser
    output_parser = StrOutputParser()

    # Chain
    # chain = create_stuff_documents_chain(
    #     llm = model,
    #     prompt = prompt,
    #     output_parser= output_parser
    # )

    retriever = vector_store.as_retriever(search_kwaargs = {"k": 5})  # Convert vector store into a retriever
    retrieval_chain = create_retrieval_chain(
        retriever, 
        chain
        )  # Create a retrieval-based chain
    
    # tool for our document 
    retriever_tool = create_retriever_tool(
    retriever,
    "toolbox_search", # identifier for the tool
    "Use this tool when searching for information about FreeSurfer" # description of the tool
    )

    # tool for our web search
    search = TavilySearchResults() 

    # List of tools - we have 2 tools here
    tools = [search, retriever_tool]

    # Create an agent that uses the LLM, prompt, and tools (no chain here)
    agent = create_openai_functions_agent(
        llm = model,
        prompt = prompt,
        tools = tools
    )

    agentExecutor = AgentExecutor(
        agent = agent,
        tools = tools
    )

    return agentExecutor  # Return the retrieval chain


# Function to ask a question
def process_chat(agentExecutor, question, history):
    response = agentExecutor.invoke({
        "input": question,
        "chat_history": history,
        "context": docs
    })

    return response["output"]


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

