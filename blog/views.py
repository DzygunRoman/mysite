from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage

def post_list(request): #представление извлечь все посты со статусом PUBLISHED
    post_list = Post.published.all()
    #Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3) #создаем экземпляр класса с числом объектов возвращаемых на страницу
    page_number = request.GET.get('page', 1) #извлекаем номер страницы и сохраняем в page_number
    try:
        posts = paginator.page(page_number) #получаем объекты для желаемой страницы и сохраняем в posts
    except EmptyPage:
        # Если номер страницы находится вне диапазона то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
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



