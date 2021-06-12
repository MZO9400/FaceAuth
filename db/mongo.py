import pymongo


class FaceEncodings:
    def __init__(self, connection_string):
        self.__client__ = pymongo.MongoClient(connection_string)
        self.collection = self.__client__['face_data']['encodings']

    def insert(self, user):
        print(user)
        if (user['username'] is not None) and (user['encodings'] is not None):
            user['encodings'] = user['encodings'].tolist()
            self.collection.insert_one(user)
            return True
        else:
            return False

    def fetch(self, username=None):
        if username:
            return self.collection.find_one({'username': username})
        else:
            return self.collection.find()

    def is_unique(self, username):
        return True if self.collection.find({'username': username}).count() == 0 else False
