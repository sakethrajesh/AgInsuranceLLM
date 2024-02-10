from ollama import Client
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# get OLLAMA_URL from environment
OLLAMA_URL = os.environ.get('OLLAMA_URL')

print(f'Using OLLAMA_URL: {OLLAMA_URL}')

client = Client(host=OLLAMA_URL)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data['messages']

    try:        
        res = client.chat(model='llama2:chat', messages=messages)

        text_content = res["message"]["content"]

        return jsonify({"text": text_content}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
