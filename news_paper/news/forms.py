from django import forms
from .models import Post


class ArticleForm(forms.ModelForm):
    type_post = Post.article

    class Meta:
        model = Post
        fields = [
            "author",
            "type_post",
            "title",
            "content"
        ]
