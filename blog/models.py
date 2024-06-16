from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self): #  метод возвращает отфильтрованные посты
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, verbose_name='Слаг')
    author = models.ForeignKey(User, verbose_name='Автор',
                               # связь данной модели с встроенной моделью User - многие к одному
                               on_delete=models.CASCADE,  # вариант удаления связанных сущностей
                               related_name='blog_posts')  # обратная связь от User к Post(user.blog_posts)
    body = models.TextField(verbose_name='Текст')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name='Статус')
    objects = models.Manager()  #  менеджер применяемый по умолчанию
    published  = PublishedManager()  #  конкретно-прикладной менеджер

    class Meta:  # это класс определяет метаданные модели
        ordering = ['-publish']  # предустановка сортировки по полю publish по умолчанию
        indexes = [
            models.Index(fields=['-publish']),  # индекс повысит скорость запросов фильтрующих по данному полю
        ]
        verbose_name = 'Пост'  #  меняю отображение слова пост в амин-панели на русский
        verbose_name_plural = 'Посты'  # множественное число

    def __str__(self):
        return self.title
