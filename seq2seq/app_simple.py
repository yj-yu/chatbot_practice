import os
import sys
import requests
import json
from PIL import ImageFile
from flask import Flask, request, make_response, jsonify

import tensorflow as tf
import data
import sys
import model as ml

from configs import DEFINES

char2idx,  idx2char, vocabulary_length = data.load_vocabulary()
# 에스티메이터 구성
classifier = tf.estimator.Estimator(
        model_fn=ml.model,
        model_dir=DEFINES.check_point_path,
        params={
            'hidden_size': DEFINES.hidden_size,
            'layer_size': DEFINES.layer_size,
            'learning_rate': DEFINES.learning_rate,
            'vocabulary_length': vocabulary_length,
            'embedding_size': DEFINES.embedding_size,
            'embedding': DEFINES.embedding,
            'multilayer': DEFINES.multilayer,
        })
predic_output_dec, predic_output_dec_length = data.dec_input_processing([""], char2idx)
predic_target_dec = data.dec_target_processing([""], char2idx)

def pred(input):
    predic_input_enc, predic_input_enc_length = data.enc_processing([input], char2idx)
    predictions = classifier.predict(
        input_fn=lambda:data.eval_input_fn(predic_input_enc, predic_output_dec, predic_target_dec, 1))# DEFINES.batch_size))
    return data.pred2string(predictions, idx2char)

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

#@app.route('/')
#def main():
#    return render_template('index.html')
if __name__ == '__main__':
    app.run(port=11111,debug=True,threaded=True)#, ssl_context='adhoc')
