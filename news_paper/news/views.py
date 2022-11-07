from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import  (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Category
from .forms import PostForm
from .filters import PostFilter, PostCategoryFilter


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')


class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = "-created_at"
    template_name = "post_list.html"
    paginate_by = 10
    context_object_name = "post_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostCategoryFilter(self.request.GET, queryset)
        print("******************** get_queryset*******************8")
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context["filterset"] = self.filterset
        category = self.request.GET.get("categories")
        if category is not None:
            context["category"] = Category.objects.get(pk=int(category))
        else:
            context["category"] = None
        return context

    def post(self, request, *args, **kwargs):
        #category : Category = context["category"]
        print(request.POST.keys())
        for val in request.POST.values():
            print(val)
        print(kwargs)
        user = request.user
        #category.subscribers.add(user)
        print(user)
        return redirect("/news")


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


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = Post.article
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Статья"
        return context


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    queryset = Post.objects.filter(type_post=Post.article)
    template_name = "post_edit.html"
    pk_url_kwarg = "id"
    permission_required = ('news.change_post',)

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


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = Post.news
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Новость"
        return context


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    queryset = Post.objects.filter(type_post=Post.news)
    pk_url_kwarg = "id"
    template_name = "post_edit.html"
    permission_required = ('news.change_post',)

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
