from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Test scripts"

    def handle(self, *args, **options):
        print('Empty')