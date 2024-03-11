from django.core.management.base import BaseCommand
from recipes_app.models import Category


class Command(BaseCommand):
    help = 'Adds categories to the database'

    def handle(self, *args, **options):
        categories = ['Завтрак', 'Обед', 'Ужин', 'Закуски', 'Супы', 'Салаты', 'Выпечка', 'Десерты', 'Напитки',
                      'Вегетарианские блюда']

        for category in categories:
            Category.objects.get_or_create(title=category)

        self.stdout.write(self.style.SUCCESS('Categories added successfully'))
