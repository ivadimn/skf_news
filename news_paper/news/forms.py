from django import forms
from .models import Post, Author, Category


class PostForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=((e.get("id"), e.get("name")) for e in Category.objects.all().values("id", "name"))
    )

    class Meta:
        model = Post
        fields = ["author", "categories", "title", "content"]
        labels = {"author": "Автор", "categories": "Категории", "title": "Заголовок", "content": "Содержимое"}

