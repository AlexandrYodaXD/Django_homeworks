from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view),
    path('index/', views.index_view),
    path('clients/', views.clients_view),
    path('products/', views.products_view),
    path('orders/', views.orders_view),
    path('order/<int:order_id>/', views.get_order_by_id_view, name='get_order_by_id'),
    path('product/<int:product_id>/', views.get_product_by_id_view, name='get_product_by_id'),
    path('client/<int:client_id>/', views.get_client_by_id_view, name='get_client_by_id'),
    path('client/<int:client_id>/statistics/', views.get_product_order_statistics_view, name='get_product_order_statistics'),
    path('client/<int:client_id>/edit', views.edit_client_view, name='edit_client'),
    path('product/<int:product_id>/edit', views.edit_product_view, name='edit_product'),
]
