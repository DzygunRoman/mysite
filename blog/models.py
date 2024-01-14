from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=250) #заголовок
    slug = models.SlugField(max_length=250) #слаг
    body = models.TextField() #тело поста
    publish = models.DateTimeField(default=timezone.now) #время публикации
    created = models.DateTimeField(auto_now_add=True) #время создания
    updated = models.DateTimeField(auto_now=True) #время изменения

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),#индексирование поля publish для ускорения выполнения запросов по этому полю
        ]


    def __str__(self):
        return self.title