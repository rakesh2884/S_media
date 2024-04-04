from django.contrib.auth.models import AbstractUser
from django.db import models
from s_media import settings

class User(AbstractUser):
    ROLES = (
        (1, 'User'),
        (2, 'Admin'),
        (3, 'Moderator'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    profile_picture = models.ImageField(upload_to=settings.UPLOAD_PROFILE_FOLDER, null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='post')
    caption = models.TextField()
    post = models.FileField(upload_to=settings.UPLOAD_POST_FOLDER, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comment_post')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_notification')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notification")
    subject = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)