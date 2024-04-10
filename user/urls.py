from django.urls import path
from user import views

urlpatterns = [
    path('register',
         views.register.as_view(),
         name='register'),
    path('login',
         views.login.as_view(),
         name='login'),
    path('profile',
         views.get_profile.as_view(),
         name='get_profile'),
    path('profile_update',
         views.update_profile.as_view(),
         name='update_profile'),
    path('change_password',
         views.change_password.as_view(),
         name='change_password'),
    path('self_profile_delete',
         views.delete_self_account.as_view(),
         name='delete_self_profile'),
    path('users/<int:user_id>/',
         views.view_others_profile.as_view(),
         name='user_profile'),
]
