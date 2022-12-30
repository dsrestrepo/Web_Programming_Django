from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

    def __str__(self):
        return f"post {self.id} by user: {self.user} at: {self.timestamp}"

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followers")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "followers": [follower.username for follower in self.followers.all()]
        }

    def __str__(self):
        return f"user {self.user} have a followers row in db"

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    users = models.ManyToManyField(User, blank=True, related_name="likes")
    
    def serialize(self):
        return {
            "id": self.id,
            "users": [user.username for user in self.users.all()],
            "post": self.post.id,
        }

    def __str__(self):
        return f"post {self.post} has a likes row in db"