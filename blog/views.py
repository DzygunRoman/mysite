from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


def post_list(request):
    posts = Post.published.all()  # извлекаются все посты при помощи ранее созданного менеджера
    return render(request, 'blog/post/list.html', {'posts': posts})  # прорисовка шаблона


def post_detail(request, id):  # извлекаю пост по id и в render отправляю в шаблон
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)  # функция либо извлекает пост либо выдает исключение
    return render(request, 'blog/post/detail.html', {'post': post})
