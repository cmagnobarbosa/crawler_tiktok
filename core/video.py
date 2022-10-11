"""Vide model"""
from datetime import datetime


class Video:

    def __init__(self, user, title, description, likes, comments, shares, date):
        self.user = user
        self.title = title
        self.description = description
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.date = date
        self.created_at = datetime.now()