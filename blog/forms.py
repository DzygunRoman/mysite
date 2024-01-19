from django import forms
from .models import Comments


class EmailPostForm(forms.Form): #формы помещают в файле forms.py приложения
    name = forms.CharField(max_length=25) #имя человека отправляющего пост
    email = forms.EmailField() #адрес отправителя поста
    to = forms.EmailField() #адрес получателя поста
    comments = forms.CharField(required=False, widget=forms.Textarea) #комментарии к посту опционально


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments #указываю модель для которой будет создана форма
        fields = ['name', 'email', 'body'] #поля взятые из этой модели для создания формы


