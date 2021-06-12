import base64
import json

import cv2
import numpy as np
from decouple import config
from flask import Flask, render_template, request

from api.face import FaceVerification
from db.mongo import FaceEncodings

app = Flask(__name__)

face_verification = FaceVerification(
    FaceEncodings(
        config("DATABASE_URI")
    )
)


@app.route('/register', methods=["POST"])
def register_post():
    username = request.form.get('username')
    image = request.form['image']
    img = base64.b64decode(image)
    img = cv2.imdecode(np.fromstring(img, np.uint8), cv2.IMREAD_ANYCOLOR)
    registration_response = face_verification.registration(image=np.array(img), username=username)
    if registration_response['success']:
        registration_response.update({"code": 200})
    else:
        registration_response.update({"code": 400})
    return json.dumps(registration_response)


@app.route('/login', methods=["POST"])
def login_post():
    username = None
    if request.form['username']:
        username = request.form.get('username')
    image = request.form['image']
    img = base64.b64decode(image)
    img = cv2.imdecode(np.fromstring(img, np.uint8), cv2.IMREAD_ANYCOLOR)
    auth_response = face_verification.authenticate(image=np.array(img), username=username)
    if auth_response['success']:
        auth_response.update({"code": 200})
    else:
        auth_response.update({"code": 400})
    return json.dumps(auth_response)
