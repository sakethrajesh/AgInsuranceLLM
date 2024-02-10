from ollama import Client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import os

OLLAMA_URL = "https://ollamaaginsurance.endeavour.cs.vt.edu/"

client = Client(host=OLLAMA_URL)

# chroma_client = chromadb.HttpClient(host='https://chromadb-ingress.endeavour.cs.vt.edu/', port=80)
# # chroma_client.reset()

file_path = './InsuranceContext/2024-18150-1-Rainfall-Index-Handbook.pdf'

# loader = PyPDFLoader(file_path)
# docs = loader.load_and_split()

# print(docs)

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
# splits = text_splitter.split_documents(docs)

# # Create Ollama embeddings and vector store
# embeddings = OllamaEmbeddings(model="mistral")
# vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, client=chroma_client, collection_name="insurance_collection")

# # Create the retriever
# retriever = vectorstore.as_retriever()

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

import os
from langchain.text_splitter import CharacterTextSplitter
import chromadb

pdf_folder_path = "./InsuranceContext"
documents = []
for file in os.listdir(pdf_folder_path):
    if file.endswith('.pdf'):
        print(file)
        pdf_path = os.path.join(pdf_folder_path, file)
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

chroma_client = chromadb.HttpClient(host='https://chromadb-ingress.endeavour.cs.vt.edu')
if chroma_client.list_collections():
    consent_collection = chroma_client.create_collection("insurance_collection2")
else:
    print("Collection already exists")
vectordb = Chroma.from_documents(
    documents=chunked_documents,
    embedding=OllamaEmbeddings(model="mistral"),
    collection_name="insurance_collection")
# return vectordb