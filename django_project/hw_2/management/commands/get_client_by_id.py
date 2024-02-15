from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from hw_2.models import Client


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int)

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']
        client = Client.objects.get(id=client_id)
        self.stdout.write(self.style.SUCCESS(f'Client {client.name} found successfully'))