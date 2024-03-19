import requests
import csv
import datetime

def evaluate(question):
    url = "http://localhost:5001/api/chat"
    data = {"messages": [{"role": "user", "content": question}]}
    # headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data)
    print(response.json(), flush=True)
    return response.json()["text"]


headers = []

with open('testbench.csv', 'r') as csv_file:
    content = csv_file.readlines()
    headers = content[:1]   
    headers = headers[0].split(',')
    headers[-1]= headers[-1].strip()

questions = headers[1:]

answers = []

current_date = datetime.date.today()
answers.append(current_date)

with open('testbench.csv', 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for question in questions:
        answer = 'evaluate(question)'

        answers.append(answer)

    csv_writer.writerows(answers)

