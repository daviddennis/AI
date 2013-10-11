from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
import csv
import sys

class Command(BaseCommand):

    def handle(self, *args, **options):

        in_file = open('/root/research/concept_map/data/dist.female.first', 'r')

        csvreader = list(csv.reader(in_file, delimiter=' '))
        for row in csvreader:
            row = [x for x in row if x != '']
            name, female_pct, male_pct, rank = row
            #female_pct, male_pct = (float(female_pct), float(male_pct))
            female_pct = 100.0
            #male_pct = 100.0
            rank = int(rank)
            person_name, created = PersonName.objects.get_or_create(
                name=name)

            # except:
            #     PersonName.objects.filter(name=name).all().delete()
            #     person_name, created = PersonName.objects.get_or_create(
            #         name=name,
            #         male_pct=male_pct,
            #         rank=rank)
            #     # female_pct=female_pct,
            #     # male_pct=male_pct,
            #     # rank=rank)

            #person_name.male_pct = male_pct
            person_name.female_pct = female_pct
            person_name.rank = rank
            #person_name.last_pct = 100.0
            person_name.save()
            print person_name

        return
