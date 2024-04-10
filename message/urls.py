from django.urls import path
from message import views

urlpatterns = [
    path('send_message/<int:user_id>/',
         views.send_message.as_view(),
         name='send_message'),
    path('delete_message/<int:sender_id>/',
         views.delete_message.as_view(),
         name='delete_message'),
    path('get_message/<int:sender_id>/',
         views.view_message.as_view(),
         name='get_message'),
    path('get_notification/',
         views.view_notifications.as_view(),
         name='get_notification'),
]
