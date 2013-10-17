from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
import sys
from wikipedia.models import *
import en

class Command(BaseCommand):

    def handle(self, *args, **options):

        concepts = Concept.objects.filter(plural_name__isnull=True).all()

        numbers = set([str(x) for x in range(10)])

        for c in concepts:
            do = True
            if not c.plural_name:
                if ' ' not in c.name:
                    for l in c.name:
                        if l in numbers:
                            do = False
                            break
                    if c.name:
                        if c.name[-1] == "S":
                            do = False
                    else:
                        do = False
                    if do:
                        try:
                            plural_name = en.noun.plural(c.name.lower()).upper()
                        except:
                            continue
                        if c.name != c.plural_name:
                            c.plural_name = plural_name
                            c.save()
                            print c.name, c.plural_name
            # else:
            #     c.plural_name = None
            #     c.save()

        return
