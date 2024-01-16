from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


def post_list(request): #представление извлечь все посты со статусом PUBLISHED
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):#извлекаем объект с заданным id, вызвав метод get() стандартного менеджера objects
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post/detail.html', {'post': post})#прорисовка извлеченного поста с использованием шаблона



