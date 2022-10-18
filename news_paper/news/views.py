from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = "-created_at"
    template_name = "news_list.html"
    context_object_name = "news_list"


class News(DetailView):
    model = Post
    template_name = "news.html"
    pk_url_kwarg = "id"
    context_object_name = "news"

