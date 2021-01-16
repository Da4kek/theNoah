import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


def speak():
    data = json.loads(open('nfL6.json','r').read())
    train = []
    for k,row in enumerate(data):
        train.append(row['question'])
        train.append(row['answer'])
    chatbot = ChatBot("Noah")
    trainer = ListTrainer(chatbot)
    trainer.train(train)
    while True:
        request = input("You: ")
        response = chatbot.get_response(request)
        print(response)

