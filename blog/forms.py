from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # имя человека отправляющего пост
    email = forms.EmailField() # почта отправившего пост
    to = forms.EmailField() # почта получателя поста
    comments = forms.CharField(required=False, widget=forms.Textarea)  #  комментарий отправленный сообщением по электронной почте

