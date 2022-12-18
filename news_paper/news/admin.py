from django.contrib import admin
from .models import Category, Post, Author


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ("type_post", "title", "author", "rating", "time_in")
    list_filter = ("type_post", "author", )
    search_fields = ("title", "author")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)

