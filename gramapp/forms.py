from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Comment



class PostForm(forms.ModelForm):
     class Meta:
        model = Post
        fields=['post_image','caption']
        # fields='_all_'
    


class CommentForm(forms.ModelForm):
     class Meta:
        model = Comment
        fields=['comment_text']
