class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def get_user(self):
        return {
            "id": self.user_id,
            "name": self.name
        }