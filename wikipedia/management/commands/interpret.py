from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.pattern_recognizer import PatternRecognizer
from wikipedia.lib.group_manager import GroupManager
from wikipedia.lib.interpreter import Interpreter
from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection, StopwordSequence, Group, GroupInstance
import sys
from annoying.functions import get_object_or_None
from text.blob import TextBlob


class Command(BaseCommand):

    def handle(self, *args, **options):
        #sentence = "The United States of America (also known as America, the U.S., or the U.S.A.) is a country on the continent of North America"
        #sentence = "Jupiter is the largest planet in the Solar System"
        #sentence = "The Sun is the star at the center of the Solar System"
        #sentence = "The Republic of India (Hindi: .... .......) is a country in Asia"
        #sentence = "A television (also TV, telly or tube) is a machine with a screen"
        #sentence = "The Moon (Latin: luna) is what people generally say when talking about Earth's satellite"
        #sentence = "There are eight planets in the Solar System"
        #sentence = "What is the number"
        sentence = "A machine is a thing"
        if args:
            sentence = ' '.join(args)

        tb = TextBlob(sentence)
        tags = tb.tags
        #print tags

        sentence = sentence.upper()

        interpreter = Interpreter()

        sentence = interpreter.parser.remove_parentheses(sentence)
        latest = [sentence]

        latest = interpreter.parser.parse(latest)

        print latest

        start = 0
        for item in latest:
            if isinstance(item, Concept):
                i = 0
                for word, pos_tag in tags[start:]:
                    if item.name == word.upper():
                        #print item, (word, pos_tag)
                        item.pos = pos_tag
                        start = i
                    i += 1

        interpreter.interpret(latest)

        return
