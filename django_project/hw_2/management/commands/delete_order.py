from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Order


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        order_id = kwargs['id']
        order = Order.objects.get(id=order_id)
        Order.objects.filter(id=order_id).delete()
        self.stdout.write(self.style.SUCCESS(f'Order with id {order_id} deleted successfully'))
