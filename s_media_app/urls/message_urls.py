from django.urls import path
from s_media_app.views import message_views

urlpatterns = [
    path('send_message/<int:user_id>/', message_views.send_message.as_view(), name='send_message'),
    path('delete_message/<int:sender_id>/', message_views.delete_message.as_view(), name='delete_message'),
    path('get_message/<int:sender_id>/', message_views.view_message.as_view(), name='get_message'),
    path('get_notification/', message_views.view_notifications.as_view(), name='get_notification'),
]