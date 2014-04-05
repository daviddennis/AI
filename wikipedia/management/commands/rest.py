from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
import sys
#from wikipedia.lib.query_mgr import QueryManager
from wikipedia.lib.word_mgr import WordManager
#from annoying.functions import get_object_or_None


class Command(BaseCommand):

    def handle(self, *args, **options):
        #x = get_object_or_None(Relation, name="HasProperty")
        #q_mgr = QueryManager()
        word_mgr = WordManager()
        return
