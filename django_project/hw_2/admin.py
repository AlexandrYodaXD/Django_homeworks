from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Client, Product, Order, OrderItem


@admin.action(description='Пометить выделенные записи как удаленные')
def set_deleted(modeladmin, request, queryset):
    queryset.update(is_deleted=True)


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email', 'phone', 'address', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at',)
    search_fields = ('name', 'id', 'email', 'phone', 'address', 'created_at', 'is_deleted')
    fields = ('id', 'name', 'email', 'phone', 'address', 'avatar', 'created_at', 'is_deleted')
    readonly_fields = ('id', 'created_at')
    ordering = ('name', 'created_at')
    actions = [set_deleted]
    inlines = [OrderInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description', 'price', 'count', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('name', 'id', 'description', 'price', 'count', 'created_at', 'is_deleted')
    fields = ('id', 'name', 'description', 'price', 'count', 'image', 'created_at', 'is_deleted')
    readonly_fields = ('id', 'created_at')
    ordering = ('name', 'created_at')
    actions = [set_deleted]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    # Метод для получения кликабельного имени клиента
    def client_name(self, obj):
        url = reverse('admin:hw_2_client_change',
                      args=[obj.client.id])
        return format_html('<a href="{}">{}</a>', url, obj.client.name)

    client_name.short_description = 'Client'

    inlines = [OrderItemInline]
    list_display = ('id', 'client_name', 'total_price', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at', 'client')
    search_fields = ('id', 'client', 'total_price', 'created_at', 'is_deleted')
    fields = ('id', 'client', 'total_price', 'created_at', 'is_deleted')
    readonly_fields = ('id', 'created_at')
    ordering = ('id', 'created_at')
    actions = [set_deleted]


admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
