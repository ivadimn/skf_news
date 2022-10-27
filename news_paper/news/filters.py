from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post, Author


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        #queryset=Author.objects.values_list("user__username", flat=True),
        lookup_expr="exact",
        field_name="author"
    )
    created_at = DateFilter(field_name="created_at", lookup_expr="gt")


    class Meta:
        model = Post
        fields = {
            "title": ["icontains"],
            #"author": ["exact"],
            #"created_at": ["gt"],
        }
