

class User:

    def __init__(self, username, following, followers, likes):
        self.username = username
        self.following = following
        self.followers = followers
        self.likes = likes
        self.created_at = datetime.now()

    def __eq__(self, other):
        return self.username == other.username