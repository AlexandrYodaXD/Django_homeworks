from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction
# noinspection PyUnresolvedReferences
from hw_2.models import Order, Product, Client


class Command(BaseCommand):
    help = 'Create an order with specified products'

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID of the client')
        parser.add_argument('products_data', nargs='+', type=str,
                            help='List of products with quantities (format: "product_id x quantity")')

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']
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

        with transaction.atomic():
            try:
                # Создаем заказ
                client = Client.objects.get(id=client_id)
                order = Order.objects.create(client=client)
                order.update_order('add', product_quantities)

                # Добавляем продукты в заказ
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(e.message))
                return

            total_price = order.total_price
            self.stdout.write(self.style.SUCCESS(f'Order {order.id} created successfully with total price {total_price}'))
