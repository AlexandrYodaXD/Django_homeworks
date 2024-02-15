from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Client


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int)
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('address', type=str)

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']
        name = kwargs['name']
        email = kwargs['email']
        phone = kwargs['phone']
        address = kwargs['address']
        client = Client.objects.get(id=client_id)
        client.name = name
        client.email = email
        client.phone = phone
        client.address = address
        client.save()
        self.stdout.write(self.style.SUCCESS(f'Client {client.name} updated successfully'))