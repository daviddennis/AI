from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        in_file = open('/root/research/concept_map/wikipedia/management/commands/adverbs.txt', 'r')
        for line in in_file:
            word = line.rstrip().upper()
            if len(word) > 1:
                a, created = Adverb.objects.get_or_create(name=word)
                print a
