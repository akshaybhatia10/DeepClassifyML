from keras.applications import inception_v3,imagenet_utils
import cv2, numpy as np
from flask import Flask, request, make_response,jsonify
import numpy as np
import json
import urllib.request
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


model = None
app = Flask(__name__,static_url_path='')

def preprocess_img(im,target_size=(299,299)):
    img=cv2.resize(im,target_size)
    img=np.divide(img,255.)
    img=np.subtract(img,0.5)
    img=np.multiply(img,2.)
    return img

def load_im_from_url(url):
    requested_url = urllib.request.urlopen(url)
    image_array = np.asarray(bytearray(requested_url.read()), dtype=np.uint8)
    print (type(image_array))
    img = cv2.imdecode(image_array, -1)
    return img

def predict(img):
    img=preprocess_img(img)
    global model
    if model is None:
        model =inception_v3.InceptionV3()
        model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
    preds = model.predict(np.array([img]))
    return imagenet_utils.decode_predictions(preds)

@app.route('/classify_system', methods=['GET'])
def classify_system():
    image_url = request.args.get('imageurl')
    #print (len(image_url))
    #image_array = np.asarray(bytearray(image_url), dtype=np.uint8)
    img = cv2.imdecode(np.ndarray(image_url)[:30], -1)
    resp=predict(img)
    result=[]
    for r in resp[0]:
        result.append({"class_name":r[1],"score":float(r[2])})
    return jsonify({'results':result})

@app.route('/classify_url', methods=['GET'])
def classify_url():
    image_url = request.args.get('imageurl')
    img=load_im_from_url(image_url)
    resp=predict(img)
    result=[]
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

