import os
import json
from ollama import Client
from flask import Flask, Response, request, jsonify, stream_with_context

app = Flask(__name__)

# get OLLAMA_URL from environment
OLLAMA_URL = os.environ.get('OLLAMA_URL')
print(f'Using OLLAMA_URL: {OLLAMA_URL}')

client = Client(host=OLLAMA_URL)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data['messages']
    res = client.chat(model='llama2:chat', messages=messages)

    try:        
        text_content = res["message"]["content"]

        return jsonify({"text": text_content}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stream_chat', methods=['POST'])
def stream_chat():
    data = request.json
    messages = data['messages']
    def generate(stream):  
        for chunk in stream:
            if chunk:
                yield (json.dumps({"text": chunk["message"]["content"]}) + "\n").encode()
    try:
        return Response(stream_with_context(generate(client.chat(model='llama2:chat', messages=messages, stream=True))),content_type='application/json')    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
