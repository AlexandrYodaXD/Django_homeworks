from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        product_id = kwargs['id']
        product = Product.objects.get(id=product_id)
        product_name = product.name
        Product.objects.filter(id=product_id).delete()
        self.stdout.write(self.style.SUCCESS(f'Product with id {product_id} and name {product_name} deleted successfully'))