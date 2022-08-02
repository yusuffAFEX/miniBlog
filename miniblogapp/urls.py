from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/', views.PostListView.as_view(), name='post-list'),
    path('bloggers/', views.AuthorListView.as_view(), name='author-list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('blogger/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
