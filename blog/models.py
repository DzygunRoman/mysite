from django.db import models
from django.utils import timezone


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:  # это класс определяет метаданные модели
        ordering = ['-publish']  # предустановка сортировки по полю publish по умолчанию
        indexes = [
            models.Index(fields=['-publish']), # индекс повысит скорость запросов фильтрующих по данному полю
        ]

    def __str__(self):
        return self.title
