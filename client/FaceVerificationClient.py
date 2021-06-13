import base64
import threading
import tkinter
import tkinter.messagebox
from requests.exceptions import ConnectionError

import cv2
import face_recognition
import requests
from PIL import ImageTk, Image

from client.VideoProcessor import VideoProcessor


def run_thread(func, args=None):
    if args is None:
        args = []
    th = threading.Thread(target=func, args=args)
    th.start()


class FaceVerificationClient:
    def __init__(self, window, window_title="Authentication Client", video_source=0, api="http://localhost:5000"):
        self.window = window
        self.window.title(window_title)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.video_source = video_source
        self.api = api

        self.vid = VideoProcessor(self.video_source)

        self.canvas = tkinter.Canvas(window, width=self.vid.width / 2, height=self.vid.height / 2)
        self.canvas.grid(column=1, row=1)

        self.btn_login = tkinter.Button(window, text="Login", width=50, command=lambda: run_thread(self.login))
        self.btn_login.grid(row=2, column=0)

        self.btn_signup = tkinter.Button(window, text="Sign up", width=50, command=lambda: run_thread(self.signup))
        self.btn_signup.grid(row=2, column=2)

        self.username_string = tkinter.StringVar(window)
        self.username_input = tkinter.Entry(window, textvariable=self.username_string)
        self.username_input.grid(row=2, column=1)

        self.photo = None
        self.last_frame = None
        self.frame_count = 0

        self.delay = 100
        self.update()

        run_thread(self.api_health_check)

        self.window.mainloop()

    def login(self):
        try:
            if self.last_frame is None:
                tkinter.messagebox.showerror(title="Authentication failed", message="Could not find image")
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
                    message=response['username'] if 'username' in response else "Username checks out"
                )
        except ConnectionError:
            tkinter.messagebox.showerror(
                title="API Failure",
                message="Backend API did not respond"
            )

    def signup(self):
        try:
            name = self.username_input.get()
            if not name:
                tkinter.messagebox.showerror(title="Registration failed", message="Username is invalid")
                self.vid.enable_video_source()
                return
            if self.last_frame is None:
                tkinter.messagebox.showerror(title="Registration failed", message="Could not find image")
                self.vid.enable_video_source()
                return
            data = {
                "username": name,
                "image": self.encode_last_frame()
            }
            response = requests.post(self.api + "/register", data=data)
            response = response.json()
            if not response['success']:
                tkinter.messagebox.showerror(
                    title="Code {}".format(response['code']),
                    message=response['error']
                )
            else:
                tkinter.messagebox.showinfo(
                    title="Success",
                    message="You have been registered"
                )
        except ConnectionError:
            tkinter.messagebox.showerror(
                title="API Failure",
                message="Backend API did not respond"
            )

    def encode_last_frame(self):
        encoded = cv2.imencode('.png', self.last_frame)
        return base64.b64encode(encoded[1])

    def process_face(self, frame):
        locations = face_recognition.face_locations(frame)
        if len(locations) == 1:
            self.last_frame = frame
            if self.username_string.get() == '':
                try:
                    data = {
                        "username": self.username_input.get(),
                        "image": self.encode_last_frame()
                    }
                    self.is_request = True
                    response = requests.post(self.api + "/login", data=data)
                    response = response.json()
                    self.is_request = False
                    if response['username']:
                        self.username_input.delete(0, tkinter.END)
                        self.username_input.insert(0, response['username'])
                except:
                    return
        else:
            self.last_frame = None

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
                run_thread(lambda: self.process_face(cv2.resize(half_image, (0, 0), fx=0.5, fy=0.5)))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(half_image))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def api_health_check(self):
        try:
            response = requests.get(self.api)
            response = response.json()
            if response['success']:
                return True
            else:
                raise Exception("Backend returned non-success value")
        except:
            tkinter.messagebox.showerror("API Failure", "Please check if backend is running and is accessible")
            return False

    def close_window(self):
        self.vid.disable_video_source()
        self.window.destroy()
