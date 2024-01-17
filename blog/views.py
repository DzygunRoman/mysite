from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


def post_list(request): #представление извлечь все посты со статусом PUBLISHED
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):#извлекаем пост с заданным cлагом и датой публикации
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post
                             # publish_year=year,
                             # publish_month=month,
                             # publish_day=day
                             )

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})#прорисовка извлеченного поста с использованием шаблона



