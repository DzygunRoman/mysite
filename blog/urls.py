from django.urls import path
from . import views


app_name = 'blog' # упорядочиваем пути в соответствии с названием приложения

urlpatterns = [
    # path('', views.post_list, name='post_list'),  # путь для всех постов
    path('', views.PostListView.as_view(), name='post_list'), # путь для всех посто на основе классов
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),  # путь для одного поста
]