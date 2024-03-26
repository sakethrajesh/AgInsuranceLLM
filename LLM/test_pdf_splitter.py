from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def split_pdf(file_path):
    """
    Split a PDF document into smaller chunks of text.

    Attempt at automatic splitting of a PDF document into smaller chunks of text to be sued to embed into vectordb

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list: A list of text chunks obtained by splitting the PDF document.
    """
    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    return splits

file_path = './handbook.pdf'
print(split_pdf(file_path))
