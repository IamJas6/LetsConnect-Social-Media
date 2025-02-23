from django import forms
from . models import *
from . models import CustomUser
from django.contrib.auth.forms import UserCreationForm


#Post Form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

#Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

#Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
