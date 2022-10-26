from django.urls import path
from .views import  (
    PostList, PostDetail, ArticleCreate, NewsCreate
)

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("<int:id>", PostDetail.as_view(), name="post_detail"),
    path("article/create/", ArticleCreate.as_view(), name="article_create"),
    path("news/create/", NewsCreate.as_view(), name="news_create"),
]
