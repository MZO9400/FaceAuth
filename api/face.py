import face_recognition

class FaceVerification:
    def __init__(self, client):
        self.client = client

    def registration(self, username, image):
        pass

    def authenticate(self, image, username = None):
        pass

    def get_facial_structure(self, image):
        return face_recognition.face_encodings(image)[0]

    def count_people_in_image(self, image):
        return len(face_recognition.face_locations(image))
