from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager): #менеджер для извлечения постов используя Post.published.all()
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.PUBLISHED) #получаем посты со статусом published

class Post(models.Model):

    class Status(models.TextChoices): #вложенный перечисляемый класс для создания поля status
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250) #заголовок
    slug = models.SlugField(max_length=250) #слаг
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') #созданние связи с встроенной таблицей User один ко многим
    body = models.TextField() #тело поста
    publish = models.DateTimeField(default=timezone.now) #время публикации
    created = models.DateTimeField(auto_now_add=True) #время создания
    updated = models.DateTimeField(auto_now=True) #время изменения
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT) #поле статус\
    objects = models.Manager() #менеджер применямый по умолчанию
    published = PublishedManager() #конкретно-прикладной менеджер

    class Meta:
        verbose_name = "Мой блог" #замена в админ-панели категории блога
        verbose_name_plural = "Мой блог" #множественное число категории
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),#индексирование поля publish для ускорения выполнения запросов по этому полю
        ]


    def __str__(self):
        return self.title