from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import  (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Author
from .forms import PostForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = "-created_at"
    template_name = "post_list.html"
    paginate_by = 10
    context_object_name = "post_list"


class PostSearch(ListView):
    model = Post
    ordering = "-created_at"
    template_name = "post_search.html"
    paginate_by = 10
    context_object_name = "post_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["filterset"] = self.filterset
        return context


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


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    queryset = Post.objects.filter(type_post=Post.article)
    template_name = "post_edit.html"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Статья"
        return context


class ArticleDelete(DeleteView):
    queryset = Post.objects.filter(type_post=Post.article)
    template_name = "post_delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("post_list")

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


class NewsUpdate(UpdateView):
    form_class = PostForm
    queryset = Post.objects.filter(type_post=Post.news)
    pk_url_kwarg = "id"
    template_name = "post_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Новость"
        return context


class NewsDelete(DeleteView):
    queryset = Post.objects.filter(type_post=Post.news)
    template_name = "post_delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("post_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Новость"
        return context
