from keras.applications import inception_v3,imagenet_utils
import cv2 
import numpy as np
from flask import Flask, request, make_response,jsonify
import numpy as np
import json
import urllib.request
from urllib.request import Request, urlopen
import base64
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import logging

model = None
app = Flask(__name__,static_url_path='')


def preprocess_img(img,target_size=(299,299)):
    if (img.shape[2] == 4):
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)    
    img = cv2.resize(img,target_size)
    img = np.divide(img,255.)
    img = np.subtract(img,0.5)
    img = np.multiply(img,2.)
    return img

def load_im_from_url(url):
    requested_url = urlopen(Request(url,headers={'User-Agent': 'Mozilla/5.0'})) 
    image_array = np.asarray(bytearray(requested_url.read()), dtype=np.uint8)
    print (image_array.shape)
    print (image_array)
    image_array = cv2.imdecode(image_array, -1)
    print (image_array.shape)
    return image_array

def load_im_from_system(url):
    image_url = url.split(',')[1]
    image_url = image_url.replace(" ", "+")
    image_array = base64.b64decode(image_url)
    #image_array = np.asarray(bytearray(image_array), dtype=np.uint8)
    image_array = np.fromstring(image_array, np.uint8)
    image_array = cv2.imdecode(image_array, -1)
    return image_array    

def predict(img):
    img=preprocess_img(img)
    print (img.shape)
    global model
    if model is None:
        model =inception_v3.InceptionV3()
        model.compile(optimizer='adam', loss='categorical_crossentropy')
    preds = model.predict(np.array([img]))
    return imagenet_utils.decode_predictions(preds)



@app.route('/classify_system', methods=['GET'])
def classify_system():
    image_url = request.args.get('imageurl')
    image_array = load_im_from_system(image_url)
    resp = predict(image_array)
    result = []
    for r in resp[0]:
        result.append({"class_name":r[1],"score":float(r[2])})
    return jsonify({'results':result})

@app.route('/classify_url', methods=['GET'])
def classify_url():
    image_url = request.args.get('imageurl')
    image_array = load_im_from_url(image_url)
    resp = predict(image_array)
    result = []
    for r in resp[0]:
        result.append({"class_name":r[1],"score":float(r[2])})
    return jsonify({'results':result})



@app.route('/classify-system', methods=['GET'])
def do_system():
    return app.send_static_file('system.html')

@app.route('/classify-url', methods=['GET'])
def do_url():
    return app.send_static_file('url.html')

@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

