from ollama import Client
import os
import json
import logging
from flask import Flask, Response, request, jsonify, stream_with_context
from chromadb import HttpClient



app = Flask(__name__)
#logging.basicConfig(level=logging.DEBUG)


# ollama setup
OLLAMA_URL = os.environ.get('OLLAMA_URL')
client = Client(host=OLLAMA_URL)
print(f'Using OLLAMA_URL: {OLLAMA_URL}')

# chromadb setup
CHROMADB_URL = os.environ.get('CHROMADB_URL')
chroma_client = HttpClient(host=CHROMADB_URL)
print(f'Using CHROMADB_URL: {CHROMADB_URL}')

# chromadb collection setup
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
collection = chroma_client.get_collection(name=COLLECTION_NAME)
print(f'Using COLLECTION_NAME: {COLLECTION_NAME}')

# system prompt
prompt = '''
 You are an agricultural insurance chatbot. 
 You should only respond to questions related to agricultural insurance with context information. 
 If there is no context information, respond to the
 user that you cannot answer their question because you do not have knowledge on the subject.
 Do not disclose that you are using an external source or context of information.
 However, you cna answer basic questions without context like what is agriculture insurance.
 You should not make any agreements or promises with the user.
'''

############################################################################################################################################################

# example of how to query from chromadb
# collection.query(
#     query_texts=query_texts,
#     n_results=n_results,
#     where=where,
#     where_document=where_document
# )

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

def ollama_llm(convo, context, stream=False, model='llama2:chat'):
    question = convo[-1]['content']
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    convo[-1]['content'] = formatted_prompt
    return client.chat(model=model, messages=convo, stream=stream)  

############################################################################################################################################################


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data['messages']
    messages.insert(0, {"role": "assistant", "content": prompt})
    model = request.json.get('model', 'llama2:chat')

    try:        
        question = messages[-1]['content']

        # get the top 3 documents from the collection that are most relevant to the question
        retrieved_docs = collection.query(
            query_texts=question,
            n_results=3,
        )

        app.logger.info(retrieved_docs)

        # formatted_context = format_docs(retrieved_docs)
        formatted_context = retrieved_docs

        text_content = ollama_llm(messages, formatted_context, model=model)

        return jsonify({"text": text_content['message']['content'], "source_tags" : retrieved_docs['metadatas'], "source_documents" : retrieved_docs['documents']}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/api/stream_chat', methods=['POST'])
def stream_chat():
    messages = request.json['messages']
    messages.insert(0, {"role": "assistant", "content": prompt})
    print(messages)
    model = request.json.get('model')
    question = messages[-1]['content'] 
    retrieved_docs = collection.query(
            query_texts=question,
            n_results=3,
        )

    #app.logger.info(retrieved_docs)
    #app.logger.info(retrieved_docs['metadatas'][0]) 
    #app.logger.info(retrieved_docs['documents'][0])

    citations = []

    for i in range(len(retrieved_docs['metadatas'][0])):
        metadata = retrieved_docs['metadatas'][0][i]
        document = retrieved_docs['documents'][0][i]
        s = f" - **Reference:** {metadata['type']} from page {metadata['page']} of section {metadata['section']}"
        if len(metadata['subsection']) > 0:
            s += f" in subsection {metadata['subsection']}"
        s += f'''\n\n - **Document:** \n {document} \n'''
        citations.append(s)


    formatted_context = retrieved_docs

    print('model:', model)

    def generate(stream):  
        for chunk in stream:
            if chunk:
                yield (json.dumps({"text": chunk["message"]["content"]}) + "x1x\n").encode()
        

        yield (json.dumps({"text" : f'''\n\n **Citations**: \n\n  {"".join(citations)}'''}) + "x1x\n").encode()
    try:
        return Response(stream_with_context(generate(ollama_llm(messages, formatted_context, stream=True, model=model))),content_type='application/json')    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
