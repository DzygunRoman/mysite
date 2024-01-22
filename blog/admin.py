from django.contrib import admin
from .models import Post, Comments


@admin.register(Post) #добавляем в админ-панель класс модели Post
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']#поля отображаемые в админ-панели
    list_filter = ['status', 'created', 'publish', 'author']#правая боковая панель для фильтрации
    search_fields = ['title', 'body'] #создание строки поиска
    prepopulated_fields = {'slug': ('title',)}#автозаполнение поля слаг
    raw_id_fields = ['author'] #создание поискового виджета по полю автор
    date_hierarchy = 'publish' #навигация по иерархии дат
    ordering = ['status', 'publish'] #сортировка по умолчанию по указанным полям


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
