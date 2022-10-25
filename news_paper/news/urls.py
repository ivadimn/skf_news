from django.urls import path
from .views import NewsList, News, ArticleCreate

urlpatterns = [
    path("", NewsList.as_view(), name="news_list"),
    path("<int:id>", News.as_view(), name="news_detail"),
    path("create/", ArticleCreate.as_view(), name="article_create"),
]
