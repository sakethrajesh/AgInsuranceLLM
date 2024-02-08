from ollama import Client
import bs4
import asyncio 
import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# get OLLAMA_URL from environment
OLLAMA_URL = " https://ollamaaginsurance.endeavour.cs.vt.edu/"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    text = data['messages']
    data = {
        "model": "llama2",
        "messages": [
            {
            "role": "user",
            "content": text
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_URL}api/chat", json=data)
        response.raise_for_status()

        res = response.json()
        text_content = res["message"]["content"]

        return jsonify({"text": text_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    


    
if __name__ == '__main__':
    app.run(debug=True)
