from django.shortcuts import render
from django.views.generic import  (
    ListView, DetailView, CreateView
)
from .models import Post
from .forms import NewsForm


# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = "-created_at"
    template_name = "news_list.html"
    paginate_by = 5
    context_object_name = "news_list"


class News(DetailView):
    model = Post
    template_name = "news.html"
    pk_url_kwarg = "id"
    context_object_name = "news"


class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = Post.article
        return super().form_valid(form)

