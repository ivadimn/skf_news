from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from random import randint


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, new_rating: int):
        self.rating = new_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    article = "ARTS"
    news = "NEWS"
    TYPES = [
        (news, "Новость"),
        (article, "Статья"),
    ]
    preview_len = 124

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=4, choices=TYPES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through="PostCategory")

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self) -> str:
        if len(self.content) > Post.preview_len:
            return "{}...".format(self.content[:124])
        else:
            return self.content

    @property
    def time_in(self):
        return self.created_at.strftime("%d.%m.%Y")

    def __str__(self):
        return "{0}, {1}\n{2}".format(self.time_in, self.title, self.preview())

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


#временные функции
def like_dislike():
    posts = Post.objects.all()
    for post in posts:
        for i in range(randint(1, 1000)):
            post.like()
        for i in range(randint(1, 900)):
            post.dislike()
    comments = Comment.objects.all()
    for comment in comments:
        for i in range(randint(1, 1000)):
            comment.like()
        for i in range(randint(1, 900)):
            comment.dislike()


# суммарный рейтинг каждой статьи автора умножается на 3;
# суммарный рейтинг всех комментариев автора;
# суммарный рейтинг всех комментариев к статьям автора.
def update_rating(author: Author):
    posts = Post.objects.filter(author=author)
    rating_posts = sum(post.rating for post in posts) * 3
    ratings = Comment.objects.filter(user=author.user).values("rating")
    rating_comments = sum([rating["rating"] for rating in list(ratings)])
    rating_post_comments = 0
    for post in posts:
        ratings = Comment.objects.filter(post=post).values("rating")
        rating_post_comments += sum([rating["rating"] for rating in list(ratings)])
    author.update_rating(rating_posts + rating_comments + rating_post_comments)


