from datetime import timedelta

from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib import messages
from hw_2.models import Client, Product, Order, OrderItem
from hw_2.forms import ClientEditForm, ProductEditForm


def index_view(request):
    return render(request, 'hw_2/index.html')


def clients_view(request):
    clients_ = Client.objects.all()
    return render(request, 'hw_2/clients.html', {'clients': clients_})


def products_view(request):
    products_ = Product.objects.all()
    return render(request, 'hw_2/products.html', {'products': products_})


def orders_view(request):
    orders = Order.objects.filter(is_deleted=False).prefetch_related('order_items')
    context = {'orders': orders}
    return render(request, 'hw_2/orders.html', context)


def get_order_by_id_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'hw_2/order.html', context=context)


def get_product_by_id_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'hw_2/product.html', context=context)


def get_client_by_id_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    context = {'client': client}
    return render(request, 'hw_2/client.html', context=context)


def get_product_order_statistics_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    # Определяем временные интервалы: за последнюю неделю, месяц и год
    end_date = timezone.now()
    start_week = end_date - timedelta(days=7)
    start_month = end_date - timedelta(days=30)  # Месяц считаем как 30 дней
    start_year = end_date - timedelta(days=365)  # Год считаем как 365 дней

    # Получаем статистику по товарам в заказах за разные временные интервалы
    product_statistics_week = get_product_statistics(client, start_week, end_date)
    product_statistics_month = get_product_statistics(client, start_month, end_date)
    product_statistics_year = get_product_statistics(client, start_year, end_date)

    # Передаем статистику в контекст для отображения на странице
    context = {
        'client': client,
        'product_statistics_week': product_statistics_week,
        'product_statistics_month': product_statistics_month,
        'product_statistics_year': product_statistics_year
    }

    return render(request, 'hw_2/product_order_statistics.html', context)


def get_product_statistics(client, start_date, end_date):
    orders = Order.objects.filter(client=client, created_at__gte=start_date, created_at__lte=end_date)
    order_items = OrderItem.objects.filter(order__in=orders)
    product_statistics = order_items.values('product__name', 'product__id').annotate(total_quantity=Sum('quantity'))
    return product_statistics


# def upload_image_view(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data['image']
#             fs = FileSystemStorage()
#             fs.save(image.name, image)
#     else:
#         form = ImageForm()
#     return render(request, 'hw_2/upload_image.html', {'form': form})


def edit_client_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        # Создаем форму на основе данных клиента и данных, отправленных пользователем
        form = ClientEditForm(request.POST, request.FILES, instance=client)
        # Проверяем, валидна ли форма
        if form.is_valid():
            # Если форма валидна, сохраняем изменения
            form.save()
            # Добавляем сообщение об успешном изменении данных
            messages.success(request, 'Данные успешно изменены!')
            # Перенаправляем пользователя на страницу с деталями клиента
            return redirect('get_client_by_id', client_id=client.id)
        else:
            # Если форма не валидна, показываем ошибки
            messages.error(request, 'Форма заполнена неверно!')
            # Отображаем шаблон с формой для редактирования клиента
            return render(request, 'hw_2/edit_page.html', context={'form': form})
    else:
        # Если запрос был отправлен методом GET (обычное отображение страницы)
        # Создаем форму на основе данных клиента
        form = ClientEditForm(instance=client)

        # Отображаем шаблон с формой для редактирования клиента
    return render(request, 'hw_2/edit_page.html', context={'form': form})


def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Создаем форму на основе данных продукта и данных, отправленных пользователем
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        # Проверяем, валидна ли форма
        if form.is_valid():
            # Если форма валидна, сохраняем изменения
            form.save()
            # Добавляем сообщение об успешном изменении данных
            messages.success(request, 'Данные успешно изменены!')
            # Перенаправляем пользователя на страницу с деталями клиента
            return redirect('get_product_by_id', product_id=product.id)
        else:
            # Если форма не валидна, показываем ошибки
            messages.error(request, 'Форма заполнена неверно!')
            # Отображаем шаблон с формой для редактирования клиента
            return render(request, 'hw_2/edit_page.html', context={'form': form})
    else:
        # Если запрос был отправлен методом GET (обычное отображение страницы)
        # Создаем форму на основе данных клиента
        form = ProductEditForm(instance=product)

        # Отображаем шаблон с формой для редактирования клиента
    return render(request, 'hw_2/edit_page.html', context={'form': form})
