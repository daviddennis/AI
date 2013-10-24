from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
import sys

class Command(BaseCommand):

    def handle(self, *args, **options):

        asses = Assertion.objects.all()
        
        for ass in asses:
            if ass.concept2:
                av, created = AssertionValue.objects.get_or_create(
                    concept=ass.concept2)
            if ass.adj2:
                av, created = AssertionValue.objects.get_or_create(
                    adj=ass.adj2)
            if not av.assertions.filter(pk=ass.id).count():
                av.assertions.add(ass)

            print ass
                
        return
