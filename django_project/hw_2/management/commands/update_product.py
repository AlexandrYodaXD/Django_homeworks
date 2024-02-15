from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('count', type=int)

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        description = kwargs['description']
        price = kwargs['price']
        count = kwargs['count']
        product = Product.objects.get(name=name)
        product.description = description
        product.price = price
        product.count = count
        product.save()
        self.stdout.write(self.style.SUCCESS(f'Product {product.name} updated successfully'))