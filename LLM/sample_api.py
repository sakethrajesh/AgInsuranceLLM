# import requests
# import json

# url = "http://localhost:5001/api/chat"

# headers = {
#     "Content-Type": "application/json"
# }

# body = {
#     "messages": [
#         {"role": "user", "content": "What is agricutlureal insurance?"}
#     ],
#     "model": "llama2:chat"
# }

# response = requests.post(url, headers=headers, data=json.dumps(body))

# if response.status_code == 200:
#     response_data = response.json()
#     assert "text" in response_data, "Response does not contain 'text'"
#     assert "source_tags" in response_data, "Response does not contain 'source_tags'"
#     assert "source_documents" in response_data, "Response does not contain 'source_documents'"
#     print(response.json())
# else:
#     print(f"Error: {response.status_code} - {response.text}")



import requests
import json

url = "http://localhost:5001/api/stream_chat"

headers = {
    "Content-Type": "application/json"
}

body = {
    "messages": [
        {"role": "user", "content": "What is agricutlureal insurance?"}
    ],
    "model": "llama2:chat"
}

response = requests.post(url, headers=headers, data=json.dumps(body), stream=True)

if response.status_code == 200:
    for line in response.iter_lines():
        # filter out keep-alive new lines
        if line:
            decoded_line = line.decode('utf-8')
            print(json.loads(decoded_line))
else:
    print(f"Error: {response.status_code} - {response.text}")

