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
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def update_total_price(self):
        total_price = sum(item.product.price * item.quantity for item in OrderItem.objects.filter(order_id=self.id))
        self.total_price = total_price
        Order.objects.filter(id=self.id).update(total_price=total_price)

    def update_order(self, operation: str, product_quantities: dict[Product, int]):
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
                            # order_items.save()
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

        self.update_total_price()

    def __str__(self):
        return f'Заказ №{self.id}. Клиент: {self.client.name}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.update_total_price()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
