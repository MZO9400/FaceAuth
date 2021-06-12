import base64
import tkinter
import tkinter.messagebox

import face_recognition
import requests
from PIL import ImageTk
from PIL import Image
import cv2


class FaceVerificationClient:
    def __init__(self, window, window_title="Authentication Client", video_source=0, api="http://localhost:5000"):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.api = api

        self.vid = VideoProcessor(self.video_source)

        self.canvas = tkinter.Canvas(window, width=self.vid.width / 2, height=self.vid.height / 2)
        self.canvas.grid(column=1, row=1)

        self.btn_login = tkinter.Button(window, text="Login", width=50, command=self.login)
        self.btn_login.grid(row=2, column=0)
        self.btn_signup = tkinter.Button(window, text="Sign up", width=50, command=self.signup)
        self.btn_signup.grid(row=2, column=2)

        self.username_string = tkinter.StringVar(window)
        self.username_input = tkinter.Entry(window, textvariable=self.username_string)
        self.username_input.grid(row=2, column=1)

        self.photo = None
        self.last_frame = None
        self.frame_count = 0

        self.delay = 100
        self.update()

        self.window.mainloop()

    def login(self):
        self.vid.disable_video_source()
        if self.last_frame is None:
            tkinter.messagebox.showerror(title="Registration failed", message="Could not find image")
            self.vid.enable_video_source()
            return
        data = {
            "username": self.username_input.get(),
            "image": self.encode_last_frame()
        }
        response = requests.post(self.api + "/login", data=data)
        response = response.json()
        if not response['success']:
            tkinter.messagebox.showerror(
                title="Code {}".format(response['code']),
                message=response['error']
            )
        else:
            tkinter.messagebox.showinfo(
                title="Success",
                message=response['username'] if response['username'] else "Username checks out"
            )
        self.vid.enable_video_source()

    def signup(self):
        pass

    def process_face(self, frame):
        locations = face_recognition.face_locations(frame)
        if len(locations) == 1:
            self.last_frame = frame

    def update(self):
        cam_response = self.vid.get_frame()
        if not cam_response:
            self.window.after(self.delay, self.update)
            return
        ret, frame = cam_response
        self.frame_count += 1
        if ret:
            half_image = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            if self.frame_count % 3 == 0 or self.last_frame is None:
                self.frame_count = 0
                self.process_face(cv2.resize(half_image, (0, 0), fx=0.5, fy=0.5))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(half_image))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


class VideoProcessor:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture()
        self.video_source = video_source
        self.enable_video_source()

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return None
        else:
            return None

    def enable_video_source(self):
        if not self.vid.isOpened():
            self.vid.open(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)

    def disable_video_source(self):
        if self.vid.isOpened():
            self.vid.release()
