from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('product_id', type=int)

    def handle(self, *args, **kwargs):
        product_id = kwargs['product_id']
        product = Product.objects.get(id=product_id)
        self.stdout.write(self.style.SUCCESS(f'Product {product.name} found successfully'))