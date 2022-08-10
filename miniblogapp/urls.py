from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/', views.PostListView.as_view(), name='post-list'),
    path('bloggers/', views.AuthorListView.as_view(), name='author-list'),
    path('password_change/', views.ChangePasswordView.as_view(), name='password_chang'),
    path('blogger/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('blogger/<int:pk>/update', views.post_user_form, name='edit-author'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<slug:slug>/comment', views.post_comment_form, name='post-comment'),
    path('<slug:slug>/post_update/', views.UpdatePost.as_view(), name='post_update'),
    path('<slug:slug>/<int:pk>', views.HideUnhiddenComment.as_view(), name='hide-comment'),
    # path('blogger/<int:pk>/edit', views.AuthorUpdateView.as_view(), name='edit_profile'),
]

