import tkinter
from PIL import ImageTk
from PIL import Image
import cv2


class FaceVerificationClient:
    def __init__(self, window, window_title="Authentication Client", video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

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

        self.delay = 1
        self.update()

        self.photo = None
        self.last_frame = None

        self.window.mainloop()

    def login(self):
        pass

    def signup(self):
        pass

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            half_image = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            self.last_frame = half_image
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(half_image))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


class VideoProcessor:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture()
        self.vid.open(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

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

    def disable_video_source(self):
        if self.vid.isOpened():
            self.vid.release()
