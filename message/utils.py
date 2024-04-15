from message.models import Notification


def notification_save(user_id, sender_id, subject):
    notification = Notification(user_id, sender_id, subject)
    notification.save()
