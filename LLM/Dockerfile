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
RUN pip install openai

COPY api.py .
COPY InsuranceContext ./
COPY InsuranceContext/handbook.pdf .
COPY testapi.py .

ENTRYPOINT ["python3", "testapi.py"]
