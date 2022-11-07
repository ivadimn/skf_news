from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):

    created_at = DateFilter(field_name="created_at", lookup_expr="gt")

    class Meta:
        model = Post
        fields = {
            "title": ["icontains"],
            "author": ["exact"],
        }


class PostCategoryFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            "categories": ["exact"],
        }
