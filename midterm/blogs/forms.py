from django import forms
from . models import Blog, Post


class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blogs title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter blogs description'}),
        }


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter posts title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type something...'}),
        }


