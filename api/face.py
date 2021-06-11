import face_recognition

class FaceVerification:
    def __init__(self, client):
        self.client = client

    def registration(self, username, image):
        pass

    def authenticate(self, image, username = None):
        if self.count_people_in_image(image) != 1:
            return {
                "success": False,
                "error": "Picture should only have one person"
            }
        unknown_encodings = self.get_facial_structure(image)
        if username:
            person = self.client.fetch(username)
            if not person:
                return {
                    "success": False,
                    "error": "Username not found"
                }
            comparison_results = face_recognition.compare_faces([person['encodings']], unknown_encodings)
            return {
                "success": comparison_results[0]
            }
        else:
            people = list(self.client.fetch())
            people_encodings = list(map(lambda row: row['encodings'], people))
            face_array = face_recognition.compare_faces(people_encodings, unknown_encodings)
            index = face_array.index(True)
            if index is not None:
                return {
                    "success": True,
                    "username": people[index]['username']
                }
            else:
                return {
                    "success": False
                }

    def get_facial_structure(self, image):
        return face_recognition.face_encodings(image)[0]

    def count_people_in_image(self, image):
        return len(face_recognition.face_locations(image))
