from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):  # менеджер для извлечения постов используя Post.published.all()
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)  # получаем посты со статусом published


class Post(models.Model):
    class Status(models.TextChoices):  # вложенный перечисляемый класс для создания поля status
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)  # заголовок
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # слаг уникальный для даты публикации
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')  # созданние связи с встроенной таблицей User один ко многим
    body = models.TextField()  # тело поста
    publish = models.DateTimeField(default=timezone.now)  # время публикации
    created = models.DateTimeField(auto_now_add=True)  # время создания
    updated = models.DateTimeField(auto_now=True)  # время изменения
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)  # поле статус\
    objects = models.Manager()  # менеджер применямый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        verbose_name = "Женщина"  # замена в админ-панели категории блога
        verbose_name_plural = "Женщины"  # множественное число категории
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
            # индексирование поля publish для ускорения выполнения запросов по этому полю
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self): #канонический url изменяем в соответсвии с представлением
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')#связь комментариев с одним постом
                                                            #related_name для связи от объекта назад к нему
    name = models.CharField(max_length=80, verbose_name='Имя автора поста')
    email = models.EmailField(verbose_name='Электронная почта')
    body = models.TextField(verbose_name='Содержимое поста')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания ')#дата и время создания комментария
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    active = models.BooleanField(default=True)#статус комментариев для управления комментариями через админ-панель

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created']#сортирует комментарии в хронологическом порядке
        indexes = [
            models.Index(fields=['created']),#индексирует поля created в возрастающем порядке
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'