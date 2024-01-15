from django.apps import AppConfig


class BlogConfig(AppConfig):
    verbose_name = "Блог" #название приложения в админ-панели
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
