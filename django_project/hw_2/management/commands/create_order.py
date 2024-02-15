from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Order


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int)
        parser.add_argument('product_id', type=int)
        parser.add_argument('total_price', type=float)

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']
        product_id = kwargs['product_id']
        total_price = kwargs['total_price']
        order = Order.objects.create(client_id=client_id, product_id=product_id, total_price=total_price)
        order.save()
        self.stdout.write(self.style.SUCCESS(f'Order {order.id} created successfully'))