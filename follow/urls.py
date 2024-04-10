from django.urls import path
from follow import views

urlpatterns = [
    path('users/<int:user_id>/follow/',
         views.follow_user.as_view(),
         name='follow_user'),
    path('users/<int:user_id>/unfollow/',
         views.unfollow_user.as_view(),
         name='unfollow_user'),
]
