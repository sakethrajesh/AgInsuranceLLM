from chromadb import Documents, EmbeddingFunction, Embeddings, HttpClient
from ollama import Client
import json

# ollama stuff
OLLAMA_URL = "https://ollamaaginsurance.endeavour.cs.vt.edu/"
OLLAMA_client = Client(host=OLLAMA_URL)


# override the EmbeddingFunction class in chromadb
class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []

        for doc in input:
            embeddings.append(embeddings(model='llama2', prompt=doc))

        return embeddings


chroma_client = HttpClient(host='https://chromadb-ingress.endeavour.cs.vt.edu')

print(chroma_client.heartbeat())

collection = chroma_client.get_or_create_collection(name="test")


def process_data():
    f = open('data.json', "r")
    data = json.loads(f.read())

    documents = []
    metadatas = []
    ids = []

    for segment in data:
        documents.append(segment['document'])
        metadatas.append(segment['metadata'])
        ids.append(segment['id'])

    return documents, metadatas, ids


def add(documents, metadatas, ids):
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )


def query_collection(query_texts, n_results, where, where_document):
    return collection.query(
        query_texts=query_texts,
        n_results=n_results,
        where=where,
        where_document=where_document
    )

