from .models import Posts
from django.forms import ModelForm, TextInput


class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content']
        widgets = {
            "title": TextInput(attrs={
                'class': "form-control",
                'placeholder': "Название"
            }),
            "content": TextInput(attrs={
                'class': "form-control",
                'placeholder': "Содержание"
            })
        }
