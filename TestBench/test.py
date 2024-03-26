import requests
import csv
import datetime
import argparse

def evaluate(question):
    url = "http://localhost:5001/api/chat"
    data = {"messages": [{"role": "user", "content": question}]}
    # headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data)
    #print(response.json(), flush=True)
    return response.json()["text"]

def mock_evaluate(question):
    return question

parser = argparse.ArgumentParser()
parser.add_argument("--header", action="store_true", help="Write a header file")
args = parser.parse_args()

if args.header:
    start_str = '''Date, Comment, What does the acronym PRF-RI mean?,What is the purpose and objective of the Rainfall Index insurance plans?,What constitutes a cause of loss under the Rainfall Index plans of insurance?,How are rainfall levels measured and recorded for PRF insurance purposes?,How does the Rainfall Index translated to indemnity payments?,Which states are eligible for the PRF program?,When did the program start?,How can I enroll in the PRF insurance program for my land?,What are the premium costs associated with PRF insurance?,How does the PRF insurance determine which weather stations data are used for my land's location?,What is the deadline for purchasing PRF insurance for the upcoming season?,In case of a drought, how quickly can I expect an indemnity payment from my PRF insurance?,Can I combine PRF insurance with other types of crop insurance I already have?,Are there specific record-keeping requirements I need to follow to maintain my eligibility for PRF insurance?,Under what authority are the RI insurance plans, including the PRF program, authorized?,How does the PRF program ensure compliance with Title VI of the Civil Rights Act of 1964?,What are the responsibilities of AIPs in offering the PRF program?,Explain the process for selecting a grid ID for PRF insurance coverage.,How is the Productivity Factor used in determining coverage under the RI plans?,How are indemnity payments determined for the RI plans?,What are the requirements for acreage reporting under the PRF program?,What steps should be taken to establish a point of reference for acreage under the RI plans?,Explain the difference between contiguous and noncontiguous acreage in the program."'''
    headers = start_str.split(",")

    with open('testbench.csv', 'w', newline='\n') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)


with open('testbench.csv', 'r') as csv_file:
    content = csv_file.readline()
    headers = content.split(',')


print(headers)
questions = headers[2:]
print(questions)
answers = []

current_date = datetime.date.today().strftime("%m/%d/%Y")
answers.append(current_date)
answers.append('')

with open('testbench.csv', 'a', newline='\n') as csv_file:
    csv_writer = csv.writer(csv_file)
    for question in questions:
        answer = evaluate(question).replace(",", "\\',\\'").replace("\n","")
        print(answer)
        answers.append(answer)

    csv_writer.writerow(answers)
