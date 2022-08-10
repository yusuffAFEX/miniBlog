from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Comment, Profile, Post


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['date', 'is_hidden']


class UpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'slug', 'content', 'is_deleted']

