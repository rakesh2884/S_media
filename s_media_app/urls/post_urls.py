from django.urls import path
from s_media_app.views import post_views

urlpatterns = [
    path('posts', post_views.get_posts.as_view(), name='list_posts'),
    path('posts/create/', post_views.create_post.as_view(), name='create_post'),
    path('posts/<int:post_id>/update/', post_views.update_post.as_view(), name='update_post'),
    path('posts/<int:post_id>/delete/', post_views.delete_post.as_view(), name='delete_post'),
    path('posts/<int:post_id>/like/', post_views.like_post.as_view(), name='like_post'),
    path('posts/<int:post_id>/comment/', post_views.comment_on_post.as_view(), name='comment_on_post'),
    path('posts/liked/', post_views.liked_posts.as_view(), name='liked_posts'),
    path('posts/commented/', post_views.commented_posts.as_view(), name='commented_posts'),
    path('feed/', post_views.feed.as_view(), name='feed'),
]