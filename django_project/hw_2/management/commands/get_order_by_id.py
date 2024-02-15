from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Order


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int)

    def handle(self, *args, **kwargs):
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)
        self.stdout.write(self.style.SUCCESS(f'Order {order.id} found successfully'))