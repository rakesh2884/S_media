from django.urls import path
from search import views

urlpatterns = [
    path('search/',
         views.search.as_view(),
         name='search'),
]
