from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Client


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        client_id = kwargs['id']
        client = Client.objects.get(id=client_id)
        client_name = client.name
        Client.objects.filter(id=client_id).delete()
        self.stdout.write(self.style.SUCCESS(f'Client with id {client_id} and name {client_name} deleted successfully'))