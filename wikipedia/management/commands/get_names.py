from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection

class Command(BaseCommand):

    def handle(self, *args, **options):
        return
