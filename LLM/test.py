from ollama import Client
# import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import os

OLLAMA_URL = "https://ollamaaginsurance.endeavour.cs.vt.edu/"

client = Client(host=OLLAMA_URL)

url= 'https://www.rma.usda.gov/Policy-and-Procedure/Insurance-Plans/Livestock-Insurance-Plans'

file_path = './InsuranceContext/2024-18150-1-Rainfall-Index-Handbook.pdf'


loader = PyPDFLoader(file_path)
docs = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Create Ollama embeddings and vector store
embeddings = OllamaEmbeddings(model="mistral")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# Create the retriever
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define the Ollama LLM function
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = client.chat(model='llama2:chat', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

# Define the RAG chain
def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = format_docs(retrieved_docs)
    return ollama_llm(question, formatted_context) + "\n\n" + formatted_context


# Continuously ask the user for input
while True:
    question = input("Enter your question (or 'q' to quit): \n  >   ")
    if question.lower() == 'q':
        break

    # Use the RAG chain
    result = rag_chain(question)
    print(result)
