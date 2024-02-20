from django.core.management.base import BaseCommand
from faker import Faker
from faker_commerce import Provider
import random
from hw_2.models import Client, Product, Order, OrderItem

TIME_DELTA_DAYS = 90  # Переменная для задания временного интервала при генерации дат, в днях
TIME_DELTA = f'-{TIME_DELTA_DAYS}d'

class Command(BaseCommand):
    help = 'Заполняет базу данных случайными данными'

    def add_arguments(self, parser):
        parser.add_argument('clients_count', type=int, help='Количество клиентов')
        parser.add_argument('products_count', type=int, help='Количество продуктов')
        parser.add_argument('orders_count', type=int, help='Количество заказов')

    def handle(self, *args, **kwargs):
        target_clients_count = kwargs['clients_count']
        target_products_count = kwargs['products_count']
        target_orders_count = kwargs['orders_count']

        fake = Faker()
        fake.add_provider(Provider)

        # Создание клиентов
        for _ in range(target_clients_count):
            client = Client.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address(),
            )
            client.created_at = fake.past_date(start_date=TIME_DELTA)
            client.save()

        # Создание товаров
        for _ in range(target_products_count):
            product = Product.objects.create(
                name=fake.ecommerce_name(),
                description=fake.catch_phrase(),
                price=random.uniform(1, 100),
                count=random.randint(0, 100),
            )
            product.created_at = fake.past_date(start_date=TIME_DELTA)
            product.save()

        # Создание заказов
        clients = Client.objects.all()
        products = Product.objects.all()

        # В ходе генерации заказов может случиться так, что не получится заполнить заказ продуктами,
        # т.к. остаток меньше нуля, и, как следствие, количество заказов меньше, чем запрошено.
        # Чтобы постараться этого избежать,
        # увеличиваем количество циклов формирования заказов до target_orders_count ** 2
        # Почему не while? Потому что можно поймать бесконечный цикл, когда все товары закончились
        current_orders_count = 0
        for _ in range(target_orders_count ** 2):
            # Если достигнуто максимальное количество заказов, прерываем цикл
            if current_orders_count >= target_orders_count:
                break

            client = random.choice(clients)  # Выбираем случайного клиента
            product_quantities = dict()  # Словарь для хранения пар идентификатора продукта и его количества
            for _ in range(random.randint(1, 5)):

                # Если продукт уже присутствует в словаре, пропускаем его, чтобы не усложнять проверку на остаток
                product = random.choice(products)
                if product in product_quantities:
                    continue

                # Получаем текущее количество продукта и добавляем его в словарь со случайным количеством
                current_quantity = product.count
                if current_quantity > 0:
                    quantity = random.randint(1, current_quantity)
                    product_quantities[product] = product_quantities.get(product, 0) + quantity

            # Если словарь не пустой, создаем заказ и заполняем его
            if product_quantities:
                order = Order.objects.create(client=client)  # Создаем заказ
                created_at = fake.past_date(start_date=TIME_DELTA)  # Создаем случайную дату
                order.created_at = created_at
                order.update_order('add', product_quantities)
                order.save()
                current_orders_count += 1

        self.stdout.write(self.style.SUCCESS('Данные успешно созданы!'))
