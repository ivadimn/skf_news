from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, new_rating: int):
        self.rating = new_rating


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


    def dislike(self):
        if self.rating > 0:
            self.rating -= 1

    def preview(self) -> str:
        if len(self.content) > Post.preview_len:
            return "{}...".format(self.content[:124])
        else:
            return self.content


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

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1


