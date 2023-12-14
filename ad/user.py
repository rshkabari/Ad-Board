class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.ads = []

    def __str__(self):
        return f"User: {self.username}"
