from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection, Verb
from sys import stdout

class Command(BaseCommand):

    def handle(self, *args, **options):
        import en
        verb_names = [v.form for v in en.wordnet.all_verbs() if ' ' not in v.form]

        #print verb_names
        for verb_name in verb_names:
            verb, created = Verb.objects.get_or_create(
                name=verb_name)
            if created:
                print 'Created %s' % verb.name
                #stdout.write('\rCreated %s' % verb.name)
                #stdout.flush()
        print '\n'
