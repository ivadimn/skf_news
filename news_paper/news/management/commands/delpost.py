from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post


class Command(BaseCommand):
    help = "Удаляет статьи указанной категории например:  python manage.py --category=Category "
    missing_args_message = 'Недостаточно аргументов'
    #requires_migrations_checks = True

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--category', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполняется при вызове вашей команды

        self.stdout.write(options['category'])

