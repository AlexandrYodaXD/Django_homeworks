from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Order


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('client_name', type=str)
        parser.add_argument('product_name', type=str)
        parser.add_argument('total_price', type=float)

    def handle(self, *args, **kwargs):
        client_name = kwargs['client_name']
        product_name = kwargs['product_name']
        total_price = kwargs['total_price']
        order = Order.objects.get(client__name=client_name, products__name=product_name)
        order.total_price = total_price
        order.save()
        self.stdout.write(self.style.SUCCESS(f'Order {order.id} updated successfully'))