from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total_price(self):
        total_price = sum(item.product.price * item.quantity for item in OrderItem.objects.filter(order_id=self.id))
        self.total_price = total_price
        Order.objects.filter(id=self.id).update(total_price=total_price)

    def create_order(self, product_quantities: dict[Product, int]):
        if not self.id:
            self.save()

        for product, quantity in product_quantities.items():
            if 0 < quantity <= product.count:
                item = OrderItem(order=self, product=product, quantity=quantity)
                product.count -= quantity  # Уменьшаем количество продукта на складе

                item.save()
                product.save()
            else:
                raise ValidationError(
                    f'Invalid quantity for product {product.name}. Current quantity: {product.count}, '
                    f'but requested quantity: {quantity}')

        self.update_total_price()  # Обновляем общую стоимость заказа

    def update_products(self, operation: str, product_quantities: dict[Product, int]):
        with transaction.atomic():
            # Получаем текущие записи о товарах в заказе
            order_items = OrderItem.objects.filter(order_id=self.id)

            for product, quantity in product_quantities.items():
                order_item = order_items.filter(product=product).first()
                if operation == 'add':
                    if 0 < quantity <= product.count:
                        if order_item is not None:
                            order_item.quantity += quantity
                            product.count -= quantity
                            order_item.save()
                            product.save()
                        else:
                            order_items.create(order=self, product=product, quantity=quantity)
                            product.count -= quantity
                            product.save()
                            order_items.save()
                    else:
                        raise ValidationError(f'Invalid quantity for product {product.name}. '
                                              f'Current quantity: {product.count}, '
                                              f'but requested quantity: {quantity}')
                elif operation == 'remove':
                    if order_item is not None:
                        # Если количество возвращаемых товаров больше количества в заказе, то выдаём ошибку
                        if quantity > order_item.quantity:
                            raise ValidationError(f'Not enough {product.name} in order')
                        order_item.quantity -= quantity
                        product.count += quantity
                        order_item.save()
                        product.save()
                    else:
                        raise ValidationError(f'Product {product.name} not found in order')
                else:
                    raise ValidationError('Invalid operation')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.update_total_price()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
