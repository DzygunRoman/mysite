from django import forms


class EmailPostForm(forms.Form): #формы помещают в файле forms.py приложения
    name = forms.CharField(max_length=25) #имя человека отправляющего пост
    email = forms.EmailField() #адрес отправителя поста
    to = forms.EmailField() #адрес получателя поста
    comments = forms.CharField(required=False, widget=forms.Textarea) #комментарии к посту опционально