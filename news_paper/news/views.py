from django.shortcuts import render
from django.views.generic import  (
    ListView, DetailView, CreateView
)
from .models import Post
from .forms import PostForm


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = "-created_at"
    template_name = "post_list.html"
    paginate_by = 5
    context_object_name = "post_list"


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "post"


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = Post.article
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Статья"
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = Post.news
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Новость"
        return context
