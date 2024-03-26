# Use a base image
FROM python:3.11

# Set the working directory
WORKDIR /app


# Install any dependencies
RUN pip install langchain
RUN pip install ollama
RUN pip install langchain_community
RUN pip install chromadb
RUN pip install pypdf
RUN pip install flask

COPY api.py .
COPY InsuranceContext ./
COPY InsuranceContext/handbook.pdf .
COPY testapi.py .

ENV OLLAMA_URL=https://ollamaaginsurance.endeavour.cs.vt.edu/
ENV CHROMADB_URL=https://chromadb-ingress.endeavour.cs.vt.edu
ENV COLLECTION_NAME=RAINFALL_INDEX_INSURANCE_STANDARDS_HANDBOOK_2024

ENTRYPOINT ["python3", "testapi.py"]
