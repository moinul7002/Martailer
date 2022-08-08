from django.urls import path
from . import views

urlpatterns = [
    path('list-of-videos/', views.VideoList.as_view(), name='list-of-videos'),
    path('search/', views.SearchView.as_view(), name='search-tags'),
]