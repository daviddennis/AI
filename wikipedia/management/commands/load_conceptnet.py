from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection, Relation, Assertion
from annoying.functions import get_object_or_None
import csv

class Command(BaseCommand):

    def handle(self, *args, **options):

        with open('/root/research/concept_map/wikipedia/management/commands/assertions.csv', 'r') as assertion_file:
            csvreader = reversed(list(csv.reader(assertion_file)))
            #i = 0
            for row in csvreader:
                concept1_name, relation_name, concept2_name, score, frequency = tuple(row)
                relation, created = Relation.objects.get_or_create(name=relation_name)
                if created:
                    print 'Created %s' % relation_name
                concept1 = get_object_or_None(Concept, name=concept1_name.upper())
                concept2 = get_object_or_None(Concept, name=concept2_name.upper())
                if concept1 and concept2:
                    assertion, created = Assertion.objects.get_or_create(
                        relation=relation,
                        concept1=concept1,
                        concept2=concept2,
                        score=score,
                        frequency=frequency)
                    if created:
                        print 'Created %s' % assertion
                
                # if i > 10000:
                #     break
                # i += 1
        return
