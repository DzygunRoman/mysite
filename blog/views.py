from django.shortcuts import render
from .models import Post
from django.http import Http404


def post_list(request):
    posts = Post.published.all()  # извлекаются все посты при помощи ранее созданного менеджера
    return render(request, 'blog/post/list.html', {'posts': posts})  # прорисовка шаблона


def post_detail(request, id): # извлекаю пост по id и в render отправляю в шаблон
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("Пост не найден.")
    return render(request, 'blog/post/detail.html', {'post': post})
