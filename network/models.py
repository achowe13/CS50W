from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='followers')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"id:{self.id}-{self.user} followed {self.following} on {self.timestamp}"
    
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='likes')
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_by')