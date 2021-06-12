import cv2


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
