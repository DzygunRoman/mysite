from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag


class PostListView(ListView):  # отображение списка постов реализованное на основе класса ListView
    queryset = Post.published.all()
    context_object_name = 'posts'  # результат запроса
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request,tag_slug=None):
    post_list = Post.published.all()  # извлекаются все посты при помощи ранее созданного менеджера
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)  # постраничная разбивка
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)  # если номер страницы не int то выдавать первую страницу
    except EmptyPage:
        posts = paginator.page(
            paginator.num_pages)  # если номер страницы находится в не диапазона то показать последнюю
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})  # прорисовка шаблона


def post_detail(request, year, month, day, post):  # извлекаю пост по id и в render отправляю в шаблон
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)  # функция либо извлекает пост либо выдает исключение
    comments = post.comments.filter(active=True) # список активных комментариев к этому посту
    form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'form': form})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'dzygun-roman@mail.ru',
                      [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})
