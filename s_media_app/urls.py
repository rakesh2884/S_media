from django.urls import path
from s_media_app import views

urlpatterns = [
    path('register', views.register.as_view(), name='register'),
    path('login', views.login.as_view(), name='login'),
    path('profile', views.get_profile.as_view(), name='get_profile'),
    path('posts', views.get_posts.as_view(), name='list_posts'),
    path('posts/create/', views.create_post.as_view(), name='create_post'),
    path('posts/<int:post_id>/update/', views.update_post.as_view(), name='update_post'),
    path('posts/<int:post_id>/delete/', views.delete_post.as_view(), name='delete_post'),
    path('posts/<int:post_id>/like/', views.like_post.as_view(), name='like_post'),
    path('posts/<int:post_id>/comment/', views.comment_on_post.as_view(), name='comment_on_post'),
    path('posts/liked/', views.liked_posts.as_view(), name='liked_posts'),
    path('posts/commented/', views.commented_posts.as_view(), name='commented_posts'),
    path('users/<int:user_id>/follow/', views.follow_user.as_view(), name='follow_user'),
    path('users/<int:user_id>/unfollow/', views.unfollow_user.as_view(), name='unfollow_user'),
    path('feed/', views.feed.as_view(), name='feed'),
    path('users/<int:user_id>/', views.user_profile.as_view(), name='user_profile'),
    path('send_message/<int:user_id>/', views.send_message.as_view(), name='send_message'),
    path('get_message/<int:sender_id>/', views.view_message.as_view(), name='get_message'),
    path('get_notification/', views.view_notification.as_view(), name='get_notification'),
]