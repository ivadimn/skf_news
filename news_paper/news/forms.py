from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Post, Author, Category


class PostForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=((e.get("id"), e.get("name")) for e in Category.objects.all().values("id", "name"))
    )

    class Meta:
        model = Post
        fields = ["author", "categories", "title", "content"]
        labels = {"author": "Автор", "categories": "Категории", "title": "Заголовок", "content": "Содержимое"}


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
