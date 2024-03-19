import requests
import json
import sys

"""
Sends a chat message to a language model API and receives a response.

This function sends a chat message to a language model API and receives a response.
It can be used to interact with the model and get answers to questions.

Usage:
- To send a single chat message and receive a response:
    python sample_api.py

- To stream chat messages and receive continuous responses:
    python sample_api.py stream
"""

headers = {
    "Content-Type": "application/json"
}
body = {
    "messages": [
        {"role": "user", "content": "What is agricultural insurance?"}
    ],
    "model": "llama2:chat"
}

if len(sys.argv) > 1 and sys.argv[1] == "stream":
    url = "http://localhost:5001/api/stream_chat"
    response = requests.post(url, headers=headers, data=json.dumps(body), stream=True)
    if response.status_code == 200:
        for line in response.iter_lines():
            # filter out keep-alive new lines
            if line:
                decoded_line = line.decode('utf-8')
                print(json.loads(decoded_line))
    else:
        print(f"Error: {response.status_code} - {response.text}")

else:
    url = "http://localhost:5001/api/chat"
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        response_data = response.json()
        assert "text" in response_data, "Response does not contain 'text'"
        assert "source_tags" in response_data, "Response does not contain 'source_tags'"
        assert "source_documents" in response_data, "Response does not contain 'source_documents'"
        print(response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")


