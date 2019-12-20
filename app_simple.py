import os
import sys
import requests
import json
from PIL import ImageFile
from flask import Flask, request, make_response, jsonify

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
# Create a new chat bot named *
chatbot = ChatBot('yj')
# Create a new Trainer
#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train(
#    "./my_corpus/korean/"
#)

def pred(inputString):
    answer = chatbot.get_response(inputString)
    return answer

app = Flask(__name__, template_folder='./')

@app.route('/')
def index():
    return 'hello'

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    req = request.get_json(force=True)
    #print(req)
    print(req)
    response = str(req['queryResult']['queryText'])
    print(response)
    response = pred(response)
    response = {'fulfillmentText':str(response)}
    return response

if __name__ == '__main__':
    app.run(port=11111,debug=True,threaded=True)#, ssl_context='adhoc')
