from ollama import Client
import os
from flask import Flask, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader

app = Flask(__name__)

# get OLLAMA_URL from environment
OLLAMA_URL = os.environ.get('OLLAMA_URL')

print(f'Using OLLAMA_URL: {OLLAMA_URL}')

client = Client(host=OLLAMA_URL)

############################################################################################################################################################
file_path = './handbook.pdf'

loader = PyPDFLoader(file_path)
docs = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Create Ollama embeddings and vector store
embeddings = OllamaEmbeddings(model="mistral", base_url=OLLAMA_URL)
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# Create the retriever
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define the Ollama LLM function
def ollama_llm(convo, context):
    question = convo[-1]['content']
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    convo[-1]['content'] = formatted_prompt
    response = client.chat(model='llama2:chat', messages=convo)
    return response['message']['content']

# Define the RAG chain
def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = format_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

############################################################################################################################################################


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data['messages']

    try:        
        # res = client.chat(model='llama2:chat', messages=messages)
        question = messages[-1]['content']
        retrieved_docs = retriever.invoke(question)
        formatted_context = format_docs(retrieved_docs)

        text_content = ollama_llm(messages, formatted_context)

        return jsonify({"text": text_content}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)