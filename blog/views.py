from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


class PostListView(ListView):  # отображение списка постов реализованное на основе класса ListView
    queryset = Post.published.all()
    context_object_name = 'posts'  # результат запроса
    paginate_by = 3
    template_name = 'blog/post/list.html'


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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED) # извлечь пост по идентификатору id

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST) # форма была передана на обработку
        if form.is_valid(): #  поля формы успешно прошли валидацию
            cd = form.cleaned_data # отправить электронное письмо # словарь полей формы и их значений
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендую вам прочитать " \
                      f"{post.title}"
            message = f"Прочитать {post.title} по ссылке {post_url}\n\n" \
                      f"{cd['name']} комментарий: {cd['comments']}"
            send_mail = (subject, message, 'dzygun-roman@mail.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})