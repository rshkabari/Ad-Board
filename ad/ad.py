import datetime

class Ad:
    def __init__(self, id, title, description, contact_info, category, user_id, timestamp):
        self.id = id
        self.title = title
        self.description = description
        self.contact_info = contact_info
        self.category = category
        self.user_id = user_id
        self.timestamp = timestamp

    def __str__(self):
        return f"Ad #{self.id}: {self.title}"

    def display_details(self):
        return f"Title: {self.title}\nDescription: {self.description}\nContact Info: {self.contact_info}\nCategory: {self.category}\nPosted by User ID: {self.user_id}\nTimestamp: {self.timestamp}"
