from django.urls import path
from s_media_app.views import search_views

urlpatterns = [
    path('search/', search_views.search.as_view(), name='search'),
]