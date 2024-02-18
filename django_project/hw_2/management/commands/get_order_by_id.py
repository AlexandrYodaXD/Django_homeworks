from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Order


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int)

    def handle(self, *args, **kwargs):
        order_id = kwargs['order_id']
        try:
            order = Order.objects.get(id=order_id)
            self.stdout.write(self.style.SUCCESS(f'Order {order.id} found successfully'))
            self.stdout.write(f'Created at: {order.created_at}')
            self.stdout.write(f'Client:'
                              f'\n-id: {order.client.id}'
                              f'\n-name: {order.client.name}')
            self.stdout.write('Products:')
            for item in order.orderitem_set.all():
                self.stdout.write(f'- {item.product.name} ({item.product.price}$): {item.quantity} PC.')
            self.stdout.write(f'Total price: {order.total_price}$')
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Order with ID {order_id} does not exist'))
            return

