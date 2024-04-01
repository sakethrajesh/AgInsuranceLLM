# LLM

## File Structure
```
.
└── LLM/
    ├── InsuranceContext/
    │   └── handbook.pdf
    │
    ├── .env.example
    ├── .gitignore
    │
    ├── api.py                  <-- main api file that facilities communication to Ollama (LLMs) and ChromaDB (vectordb)
    ├── Dockerfile              <-- dockerfile, instructions to create environment that runs the api.py
    ├── docker-compose.yaml     <-- compose file that can be used to run Dockerfile
    ├── dockerpush.sh           <-- script to push api Docker image to container registry
    ├── sample_api.py           <-- 
    ├── test_pdf_splitter.py    <-- 
    └── testapi.py              <-- same functionality of api.py, but has alternate segmentation methods
```

## API Reference
This documentation provides information about the endpoints available in the Flask app.

### Chat

```http
  POST /api/chat
```

| Parameter | Type     | Description                                   |
| :-------- | :------- | :-------------------------------------------- |
| `messages`| `array`  | **Required**. Array of user's messages        |
| `model`   | `string` | Optional. Model for chat (default: llama2:chat)|

``` json
{
    "messages": [
        {
            "role": "user",
            "content": "User's message"
        }
    ],
    "model": "llama2:chat"  // Optional, default is "llama2:chat"
}
```

#### Success Response

 **Code:** `200 OK`
 **Content:** 
  ```json
  {
      "text": "Assistant's response",
      "source_tags": ["source_tag_1", "source_tag_2"],
      "source_documents": ["source_document_1", "source_document_2"]
  }
  ```

#### Error Response

 **Code:** `500 Internal Server Error`
 **Content:** 
  ```json
  {
      "error": "Error message"
  }
  ```

### Stream Chat

```http
  POST /api/stream_chat
```

| Parameter | Type     | Description                                   |
| :-------- | :------- | :-------------------------------------------- |
| `messages`| `array`  | **Required**. Array of user's messages        |
| `model`   | `string` | Optional. Model for chat                      |

``` json
{
    "messages": [
        {
            "role": "user",
            "content": "User's message"
        }
    ],
    "model": "llama2:chat"  // Optional, default is "llama2:chat"
}
```

#### Success Response

 **Code:** `200 OK`
 **Content:** Stream of JSON objects containing assistant's responses and citations.

 # ADD A EXAMPLE OF WHAT A STREAM LOOKS LIKE HERE

 ``` json
 {}
 ```

#### Error Response

 **Code:** `500 Internal Server Error`
 **Content:** 
  ```json
  {
      "error": "Error message"
  }
  ```

**Note:** In both endpoints, the assistant's response is generated based on the user's message and context information from relevant documents retrieved from CHROMADB. If an error occurs during the process, an error message is returned.

## env file
Create .env file and copy contents of .env.example into .env

assign these values

```
# this is the URL of the Ollama API
OLLAMA_URL=https://ollamaaginsurance.endeavour.cs.vt.edu/

# this is the URL of the vector database (ChromaDB)
CHROMADB_URL=https://chromadb-ingress.endeavour.cs.vt.edu

# this is the name of the collection in the vector database (ChromaDB)
COLLECTION_NAME=RAINFALL_INDEX_INSURANCE_STANDARDS_HANDBOOK_2024
```


## Running Locally
```bash 
docker compose up --build
```


## Pushing to Container Registry

Open dockerpush.sh

```bash
# set these variables
registry=""
username=""
project=""
serviceName=""

```

### What is happening under the hood?
This is an example
```bash
#!/bin/bash

# Define these variables
registry="container.cs.vt.edu"
username="saketh"
project="aginsurancellm"
serviceName="backend"

# login to the container registry
docker login $registry

# Build the image for a linux/amd64 platform 
docker build --platform linux/amd64 -t $registry/$username/$project/$serviceName .

# Push the image
docker push $registry/$username/$project/$serviceName
```

### To execute the push to the container registry
```bash
bash dockerpush.sh
```

## Known Issues




