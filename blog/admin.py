from django.contrib import admin
from .models import Post

admin.register(Post)  # регистрирую модель Post в админ-панели


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']  #задаем поля модели для отображения на админ-панели
