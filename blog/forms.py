from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)  # имя человека отправляющего пост
    email = forms.EmailField()  # почта отправившего пост
    to = forms.EmailField()  # почта получателя поста
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)  # комментарий отправленный сообщением по электронной почте
