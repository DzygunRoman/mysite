from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.published.all() # извлекаются все посты при помощи ранее созданного менеджера
    return render(request, 'blog/post/list.html', {'posts': posts})  # прорисовка шаблона

