from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger


def post_list(request):
    post_list = Post.published.all()  # извлекаются все посты при помощи ранее созданного менеджера
    paginator = Paginator(post_list, 3)  # постраничная разбивка
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)  # если номер страницы не int то выдавать первую страницу
    except EmptyPage:
        posts = paginator.page(
            paginator.num_pages)  # если номер страницы находится в не диапазона то показать последнюю
    return render(request, 'blog/post/list.html', {'posts': posts})  # прорисовка шаблона


def post_detail(request, year, month, day, post):  # извлекаю пост по id и в render отправляю в шаблон
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)  # функция либо извлекает пост либо выдает исключение
    return render(request, 'blog/post/detail.html', {'post': post})
