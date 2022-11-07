from django.urls import path
from .views import  (
    PostList, PostDetail, ArticleCreate, NewsCreate, ArticleUpdate, NewsUpdate,
    ArticleDelete, NewsDelete, PostSearch, upgrade_me
)

urlpatterns = [
    path("news/", PostList.as_view(), name="post_list"),
    path("news/search/", PostSearch.as_view(), name="post_search"),
    path("<int:id>", PostDetail.as_view(), name="post_detail"),
    path("article/create/", ArticleCreate.as_view(), name="article_create"),
    path("article/<int:id>/update/", ArticleUpdate.as_view(), name="article_update"),
    path("article/<int:id>/delete/", ArticleDelete.as_view(), name="article_delete"),
    path("news/create/", NewsCreate.as_view(), name="news_create"),
    path("news/<int:id>/update/", NewsUpdate.as_view(), name="news_update"),
    path("news/<int:id>/delete/", NewsDelete.as_view(), name="news_delete"),
    path('news/upgrade/', upgrade_me, name='upgrade')
]
