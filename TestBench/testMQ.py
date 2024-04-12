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

output_file = 'output.json'
questions = []
models = []

if args.header:
    # Read the JSON file
    with open('test_bench_settings.json') as json_file:
        data = json.load(json_file)

    # Extract the questions and models array
    questions = data['questions']
    models = data['models']

    # Join the questions with comma
    commaQ = ', '.join(questions)
    commaM = ', '.join(models)

commaQSplit = commaQ.split(",")
commaMSplit = commaM.split(",")
print(commaQ)
print(questions)
answers = []
json_data = []

with open('testMQtoCSV.csv', 'w', newline='\n') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Question', 'Answer', 'Model', 'Rank'])  # Write header row
    for model in models:
        question_count = 0  # Counter to track the number of questions asked for each model
        for question in commaQSplit:
            answer = evaluate(question, model).replace(",", "\\',\\'").replace("\n","")
            print(answer)
            csv_writer.writerow([question, answer, model, 0])
            json_data.append({
                "Question": question,
                "Answer": answer,
                "Model": model,
                "Rank": 0
            })
            question_count += 1
            if question_count >= 3:  # Only ask the first 3 questions
                break

print("CSV and JSON files created successfully.")

# Write JSON data to output file
with open('testMQtoJSON.json', 'w') as json_output_file:
    json.dump(json_data, json_output_file, indent=4)

print("JSON file created successfully.")