from django.urls import path
from s_media_app.views import follow_views

urlpatterns = [
    path('users/<int:user_id>/follow/',
         follow_views.follow_user.as_view(),
         name='follow_user'),
    path('users/<int:user_id>/unfollow/',
         follow_views.unfollow_user.as_view(),
         name='unfollow_user'),
]
