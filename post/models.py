from django.db import models
from user.models import User
from s_media import settings


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='post')
    caption = models.TextField()
    post = models.FileField(upload_to=settings.UPLOAD_POST_FOLDER,
                            null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='likes_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comment_post')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
