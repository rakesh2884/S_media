from django.urls import path
from s_media_app.views import user_views

urlpatterns = [
    path('register', user_views.register.as_view(), name='register'),
    path('login', user_views.login.as_view(), name='login'),
    path('profile', user_views.get_profile.as_view(), name='get_profile'),
    path('profile_update',user_views.update_profile.as_view(),name='update_profile'),
    path('self_profile_delete', user_views.delete_self_account.as_view(), name='delete_self_profile'),
    path('users/<int:user_id>/', user_views.user_profile.as_view(), name='user_profile'),
]