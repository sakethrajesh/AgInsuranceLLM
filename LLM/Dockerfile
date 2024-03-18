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
# RUN pip install pysqlite3-binary

COPY api.py .
COPY InsuranceContext ./
COPY InsuranceContext/handbook.pdf .
COPY api_unstable.py .

ENV OLLAMA_URL=https://ollamaaginsurance.endeavour.cs.vt.edu

ENTRYPOINT ["python3", "api.py"]
