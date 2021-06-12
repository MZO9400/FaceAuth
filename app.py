import numpy as np
from PIL import Image
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


@app.route("/register", methods=["GET"])
def register_get():
    return render_template('authenticate.html', URL='/register')


@app.route('/register', methods=["POST"])
def register_post():
    username = request.form.get('username')
    image = request.files['image']
    img = Image.open(image).convert('RGB')
    registration_response = face_verification.registration(image=np.array(img), username=username)
    if registration_response['success']:
        return render_template('success.html', data=registration_response)
    return render_template('failure.html', data=registration_response)


@app.route("/login", methods=["GET"])
def login_get():
    return render_template('authenticate.html', URL='/login')


@app.route('/login', methods=["POST"])
def login_post():
    username = None
    if request.form['username']:
        username = request.form.get('username')
    image = request.files['image']
    img = Image.open(image).convert('RGB')
    auth_response = face_verification.authenticate(image=np.array(img), username=username)
    if auth_response['success']:
        return render_template('success.html', data=auth_response)
    return render_template('failure.html', data=auth_response)
