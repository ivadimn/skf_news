from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post, PostCategory


class Command(BaseCommand):
    help = "Удаляет статьи указанной категории например:  python manage.py --category=Category "
    missing_args_message = 'Недостаточно аргументов'
    #requires_migrations_checks = True

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--category', type=str)

    def handle(self, *args, **options):

        category_name = options.get("category")
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                post_cats = PostCategory.objects.filter(category=category)
                count = len(post_cats)
                for post_cat in post_cats:
                    post = post_cat.post
                    post.delete()
                    post.save()
                self.stdout.write(self.style.SUCCESS("Успешно удален {} статей!".format(count)))
            except Category.DoesNotExist:
                raise CommandError("Категория: '{0}' не существует!!".format(category_name))



