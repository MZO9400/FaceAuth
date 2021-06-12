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


@app.route("/")
def hello():
    return render_template('authenticate.html')


@app.route('/register', methods=["POST"])
def register():
    username = request.form.get('username')
    img = np.fromstring(request.form.get("image"), np.uint8)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    face_verification.registration(img, username)
    return 200
