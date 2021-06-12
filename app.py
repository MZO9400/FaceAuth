import cv2
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


@app.route("/")
def hello():
    return render_template('authenticate.html')


@app.route('/register', methods=["POST"])
def register():
    username = request.form.get('username')
    image = request.files['image']
    img = Image.open(image).convert('RGB')
    registration_response = face_verification.registration(image=np.array(img), username=username)
    print(registration_response)
    if registration_response['success']:
        return {"code": 200}
    return {"code": 400, "error": registration_response['error']}
