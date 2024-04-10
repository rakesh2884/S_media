from django.db import models
from user.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="received_messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='received_notification')
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="sent_notification")
    subject = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
