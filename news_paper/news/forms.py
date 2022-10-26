from django import forms
from .models import Post, Author


class NewsForm(forms.ModelForm):
    # author = forms.ModelMultipleChoiceField(
    #     queryset=Author.objects.all().values("user.username")
    # )

    class Meta:
        model = Post
        fields = [
            "author",
            "categories",
            "title",
            "content"
        ]
