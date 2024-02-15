from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Client


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('address', type=str)

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        email = kwargs['email']
        phone = kwargs['phone']
        address = kwargs['address']
        client = Client.objects.create(name=name, email=email, phone=phone, address=address)
        client.save()
        self.stdout.write(self.style.SUCCESS(f'Client {client.name} created successfully'))