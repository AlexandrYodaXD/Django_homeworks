from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction
# noinspection PyUnresolvedReferences
from hw_2.models import Order, Product


class Command(BaseCommand):
    help = 'Add or remove products from an order'

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='ID of the order')
        parser.add_argument('operation', type=str, help='Operation to perform: add or remove')
        parser.add_argument('products_data', nargs='+', type=str,
                            help='List of products with quantities (format: "product_id x quantity")')

    def handle(self, *args, **kwargs):
        order_id = kwargs['order_id']
        operation = kwargs['operation']
        products_data = kwargs['products_data']

        # Создаем словарь для хранения пар идентификатора товара и его количества
        product_quantities = dict()

        # Заполняем словарь пар идентификатора продукта и его количества
        for product in products_data:
            try:
                product_id, quantity = map(int, product.split('x'))
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid product data'))
                return
            try:
                product = Product.objects.get(id=product_id)
                product_quantities[product] = product_quantities.get(product, 0) + quantity
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f'Product with ID {product_id} does not exist'))
                return

        # Запрашиваем информацию о заказе
        try:
            order = Order.objects.get(id=order_id)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Order with ID {order_id} does not exist'))
            return

        # Выполняем операцию над заказом
        with transaction.atomic():
            try:
                if operation in ['add', 'remove']:
                    order.update_products(operation, product_quantities)
                    self.stdout.write(self.style.SUCCESS(f'Order {order.id} updated successfully'))
                else:
                    self.stdout.write(self.style.ERROR('Invalid operation'))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(e.message))
                return

