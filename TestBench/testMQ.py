import requests
import csv
import datetime
import argparse
import json

def evaluate(question, model):
    url = "http://localhost:5001/api/chat"
    data = {"messages": [{"role": "user", "content": question, "model": model}]}
    # headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data)
    #print(response.json(), flush=True)
    return response.json()["text"]

def mock_evaluate(question):
    return question

parser = argparse.ArgumentParser()
parser.add_argument("--header", action="store_true", help="Write a header file")
args = parser.parse_args()

questions = []
models = []


with open('test_bench_settings.json') as json_file:
    data = json.load(json_file)

# Extract the questions and models array
questions = data['questions']
models = data['models']

print("Questions: ", questions)

answers = []
json_data = []

i = 0
for question in questions:
    for model in models:
        answer = evaluate(question, model)
        json_data.append({
            "Question": question,
            "Answer": answer,
            "Model": model,
            "Rank": 0
        })
    if i == 3:
        break

current_datetime = datetime.datetime.now()
filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + ".json"

with open(filename, 'w') as json_output_file:
    json.dump(json_data, json_output_file, indent=4)

print("JSON file created successfully.")