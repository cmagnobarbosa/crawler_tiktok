from datetime import datetime

class Comments:
    def __init__(self, user, comments):
        self.user = user
        self.comments = comments
        self.created_at = datetime.now()

    def __str__(self):
        return self.comments
