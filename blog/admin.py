from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)  # регистрирую модель Post в админ-панели
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']  #задаем поля модели для отображения на админ-панели
    list_filter = ['status', 'created', 'publish', 'author'] # создается боковая панель для фильтрации по указанным полям
    search_fields = ['title', 'body'] # создается строка поиска по указанным полям
    prepopulated_fields = {'slug': ('title',)} #  при вводе заголовка нового поста слаг заполняется автоматически
    raw_id_fields = ['author']
    date_hierarchy = 'publish' # поиск по датам
    ordering = ['status', 'publish'] # задается порядок сортировки по умолчанию


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']