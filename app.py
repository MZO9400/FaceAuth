from flask import Flask, render_template, request, jsonify
from PIL import Image
from api.face import FaceVerification
from db.mongo import FaceEncodings
from decouple import config
import cv2
import numpy

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
    img = Image.open(request.files["image"])
    img = np.array(img)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    face_verification.registration(img, request.form["username"])
    return 200
