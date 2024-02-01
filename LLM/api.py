import ollama
import bs4
import asyncio 
from flask import Flask, request, jsonify, stream_with_context
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
import requests

app = Flask(__name__)

docker_url = ""
client = Client(host=docker_url)

@app.route('/api/chat', methods=['POST'])
async def chat():
    data = request.get_json()
    text = data['messages']
    def generate():
        response = client.chat(model='llama2', messages=[{'role': 'user', 'content': messages}], stream=True)

    return app.response_class(stream_with_context(generate()))


    


    
if __name__ == '__main__':
    app.run(debug=True)
