from django import forms
from hw_2.models import Client, Product


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address', 'avatar', 'is_deleted']


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'count', 'image', 'is_deleted']