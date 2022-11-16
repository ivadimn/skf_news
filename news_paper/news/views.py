from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import  (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.template.loader import render_to_string
from .models import Post, Category, CategoryUser
from .forms import PostForm
from .filters import PostFilter, PostCategoryFilter
from .mail import Mail
from .tasks import hello, printer



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
        hello.delay()
        printer.apply_async([10], countdown = 5)
        queryset = super().get_queryset()
        self.filterset = PostCategoryFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context["filterset"] = self.filterset
        category_id = self.request.GET.get("categories")
        if category_id is not None:
            context["category"] = Category.objects.get(pk=int(category_id))
        else:
            context["category"] = None
        return context

    def post(self, request, *args, **kwargs):
        category_id = self.request.GET.get("categories")
        user = request.user
        if category_id is not None:
            category = Category.objects.get(pk=int(category_id))
            category.subscribers.add(user)
            category.save()
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
        #email_list = self.get_email_list(form.cleaned_data.get("categories"), post)
        #self.send_email(post, email_list)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_post'] = "Новость"
        return context

    def send_email(self, post: Post, email_list: list):
        with Mail("pickup.music@mail.ru") as mail:
            for email in email_list:
                mail.prepare_html(email[1], email[2])
                mail.send(email[0])

    def get_email_list(self, categories, post: Post) -> list:
        emails_list = []
        for cat in categories:
            for cat_user in CategoryUser.objects.filter(category=cat):
                emails_list.append((cat_user.user.email, post.title, render_to_string(
                        'news_created.html',
                         {
                            'post': post,
                            'user': cat_user.user.username
                         }
                )))
        return emails_list


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
