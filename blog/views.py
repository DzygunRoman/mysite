from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


def post_share(request, post_id):
    #извлечь пост по id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)#функция сокращенного доступа
    if request.method == 'POST':
        #форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #поля формы успешно прошли валидацию
            cd = form.cleaned_data#извлечение данных из формы
            #отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})


class PostListViews(ListView):
    #Альтернативное представление списка постов на основе класса
    queryset = Post.published.all() # queryset реализует конкретно-прикладной набор запросов
    context_object_name = 'posts' # используется для результатов запроса, если не указано имя контекстного объекта
                                  # context_object_name = <имя здесь>, то по умлчанию используется переменная object_list
    paginate_by = 3 # задается постраничная разбивка результатов с возвратом трех объектов на страницу
    template_name = 'blog/post/list.html' #прикладной шаблон используется для прорисовки страницы шаблоном template_name
                                          #если шаблон не задан, то по умолчанию ListView будет использовать blog/post_list.html

def post_list(request): #представление извлечь все посты со статусом PUBLISHED
    post_list = Post.published.all()
    #Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3) #создаем экземпляр класса с числом объектов возвращаемых на страницу
    page_number = request.GET.get('page', 1) #извлекаем номер страницы и сохраняем в page_number
    try:
        posts = paginator.page(page_number) #получаем объекты для желаемой страницы и сохраняем в posts
    except PageNotAnInteger:
        # Если номер страницы не целое число то выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы находится вне диапазона то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})# адрес расположения данного тимплейта


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



