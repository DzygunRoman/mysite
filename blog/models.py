from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):  # метод возвращает отфильтрованные посты
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, verbose_name='Слаг', unique_for_date='publish')  # слаг уникальный
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
    objects = models.Manager()  # менеджер применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:  # это класс определяет метаданные модели
        ordering = ['-publish']  # предустановка сортировки по полю publish по умолчанию
        indexes = [
            models.Index(fields=['-publish']),  # индекс повысит скорость запросов фильтрующих по данному полю
        ]
        verbose_name = 'Пост'  # меняю отображение слова пост в амин-панели на русский
        verbose_name_plural = 'Посты'  # множественное число

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])  # динамически сформированный адрес

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments' )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f"Комментарий {self.name} на {self.post}"
