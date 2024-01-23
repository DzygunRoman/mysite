from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector

def post_share(request, post_id):
    # извлечь пост по id
    post = get_object_or_404(Post, id=post_id, \
                             status=Post.Status.PUBLISHED)  # функция сокращенного доступа

    sent = False

    if request.method == 'POST':
        # форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # поля формы успешно прошли валидацию
            cd = form.cleaned_data  # извлечение данных из формы
            post_url = request.build_absolute_uri(post.get_absolute_url())  # отправить электронное письмо
            subject = f"{cd['name']} рекомендовал Вам прочитать " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'dzygun-roman@mail.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


class PostListViews(ListView):
    # Альтернативное представление списка постов на основе класса
    queryset = Post.published.all()  # queryset реализует конкретно-прикладной набор запросов
    context_object_name = 'posts'  # используется для результатов запроса, если не указано имя контекстного объекта
    # context_object_name = <имя здесь>, то по умлчанию используется переменная object_list
    paginate_by = 3  # задается постраничная разбивка результатов с возвратом трех объектов на страницу
    template_name = 'blog/post/list.html'  # прикладной шаблон используется для прорисовки страницы шаблоном template_name
    # если шаблон не задан, то по умолчанию ListView будет использовать blog/post_list.html


def post_list(request, tag_slug=None):  # представление извлечь все посты со статусом PUBLISHED
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)  # создаем экземпляр класса с числом объектов возвращаемых на страницу
    page_number = request.GET.get('page', 1)  # извлекаем номер страницы и сохраняем в page_number
    try:
        posts = paginator.page(page_number)  # получаем объекты для желаемой страницы и сохраняем в posts
    except PageNotAnInteger:
        # Если номер страницы не целое число то выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы находится вне диапазона то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})  # адрес расположения данного тимплейта


def post_detail(request, year, month, day, post):  # извлекаем пост с заданным cлагом и датой публикации
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    comments = post.comments.filter(active=True) #Список активных комментариев к этому посту
    form = CommentForm() #Форма для комментирования пользователями

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})  # прорисовка извлеченного поста с использованием шаблона


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None #переменная для хранения комментария
    # комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)  # Создать объект класса Comments, не сохраняя его в базе данных
        comment.post = post  # Назначить пост комментарию
        comment.save()  # Сохранить комментарий в БД
    return render(request, 'blog/post/comment.html', {'post': post,
                                                      'form': form,
                                                      'comment': comment})


def post_search(request):
    form = SearchForm()#создается экземпляр формы
    query = None
    results = []

    if 'query' in request.GET: #для того чтобы форма была передана на обработку в словаре request.GET отыскивается параметр query
        form = SearchForm(request.GET) #создается экземпляр формы используя переданные данные в запросе GET
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query) #выполняется поиск опубликованных постов по полям title body

    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})