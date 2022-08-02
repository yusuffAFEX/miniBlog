from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Comment, Profile


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['date']


class UpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
