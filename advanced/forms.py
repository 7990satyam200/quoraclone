from django.forms import ModelForm
from .models import Topic, Post
from django import forms

class newTopicForm(ModelForm):
    message =forms.CharField(
        widget = forms.Textarea(
            attrs={ 'placeholder':'What is on your mind?'}
            ),
    max_length = 4000,
    help_text = 'The max length of text is 4000')
    class Meta:
        model = Topic
        fields = ['subject', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
