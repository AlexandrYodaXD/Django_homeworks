import random
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from faker import Faker
from faker_commerce import Provider
from hw_2.models import Client, Product, Order

TIME_DELTA = f'-{90}d'  # Переменная для задания временного интервала при генерации дат, в днях


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

        faker = Faker()
        faker.add_provider(Provider)

        # Создание клиентов
        for _ in range(target_clients_count):
            client = Client.objects.create(
                name=faker.name(),
                email=faker.email(),
                phone=faker.phone_number(),
                address=faker.address(),
            )
            client.created_at = get_aware_time(TIME_DELTA, faker)
            client.save()

        # Создание товаров
        for _ in range(target_products_count):
            product = Product.objects.create(
                name=faker.ecommerce_name(),
                description=faker.catch_phrase(),
                price=random.uniform(1, 100),
                count=random.randint(1, 1000),
            )
            product.created_at = get_aware_time(TIME_DELTA, faker)
            product.save()

        clients = Client.objects.all()
        products = Product.objects.filter(count__gt=0)

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
                if product.count == 1:
                    quantity = 1
                else:
                    quantity = random.randint(1, product.count)
                product_quantities[product] = product_quantities.get(product, 0) + quantity

            # Если словарь не пустой, создаем заказ и заполняем его
            if product_quantities:
                order = Order.objects.create(client=client)  # Создаем заказ
                created_at = get_aware_time(TIME_DELTA, faker)  # Создаем случайную дату
                order.created_at = created_at  # Явно указываем дату создания
                order.save()  # Сохраняем заказ для сохранения даты создания
                order.update_order('add', product_quantities)  # Заполняем заказ продуктами
                current_orders_count += 1  # Увеличиваем счетчик заказов
                products = Product.objects.filter(
                    count__gt=0)  # Обновляем объект запроса, чтобы исключить продукты с нулевым остатком

        self.stdout.write(self.style.SUCCESS('Данные успешно созданы!'))


def get_aware_time(start_date, faker):
    """
    Преобразует случайную прошлую дату в "осведомленное" время.

    Args:
        start_date (str): Начальная дата для генерации случайной прошлой даты.
        faker (Faker): Генератор случайных данных.

    Returns:
        datetime: "Осведомленное" время, соответствующее случайной прошлой дате.
    """
    # Получаем случайную прошлую дату как "наивный" объект времени
    past_date = faker.past_datetime(start_date=start_date)

    # Преобразуем "наивный" объект времени в "осведомленное" время
    aware_time = make_aware(datetime.combine(past_date, datetime.min.time()))

    return aware_time
