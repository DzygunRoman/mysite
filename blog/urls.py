from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'  # определяем именное пространство приложения приложения

urlpatterns = [
    # представления поста
    path('', views.post_list, name='post_list'), #путь если метод
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListViews.as_view(), name='post_list'), #путь если используем класс
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),  # <> - для захвата значений из url-адреса
    path('<int:post_id>/share/', views.post_share, name='post_share'),#шаблон почты
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
