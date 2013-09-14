from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection, Assertion, Relation
from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.interpreter import Interpreter
from wikipedia.lib.query_mgr import QueryManager
from wikipedia.lib.nlp_gen import NLPGenerator
from sys import stdout
from time import sleep


class Command(BaseCommand):

    computer_mind = {}
    user_mind = {}

    def handle(self, *args, **options):
        interpreter = Interpreter()
        query_mgr = QueryManager()
        nlp_generator =  NLPGenerator()

        #tb = TextBlob(sentence)
        #tags = tb.tags

        print 'Hello'
        text = ''
        
        while True:
            print '> ',
            text = raw_input().upper()
            if text.lower() in ('bye', 'off', 'later', 'cya', 'end', 'e', 'goodbye'):
                break
            
            # if 'WHAT IS' in text or 'WHAT ARE' in text:
            #     tokens = interpreter.parser.tokenize(text)
            #     item_name = tokens[-1]
            #     if item_name in self.computer_mind:
            #         print '%s is %s' % (item_name, self.computer_mind[item_name])
            #         continue

            sentence = interpreter.parser.remove_parentheses(text)
            latest = [sentence]
            latest = interpreter.parser.parse(latest)

            interpreter.interpret(latest)
            #self.store_concepts(latest)

            if query_mgr.is_query(latest):
                query = query_mgr.construct_query(latest)
                answer = query_mgr.process_query(query)
                answer_sentence = nlp_generator.deparse(answer)
                print '\n:: %s\n' % (answer_sentence)

        print '\ngoodbye.\n'
        return


    def store_concepts(self, parsed_sentence):
        for item in parsed_sentence:
            if isinstance(item, Concept):
                self.computer_mind[item.name] = item

    def print_what_i_know(self):
        for key, val in self.computer_mind.iteritems():
            print 'I know that %s is %s.' % (key.lower(), val.lower())
        return



            # if 'IS' in text:
            #     is_index = text.index('IS')
            #     tokens = self.parser.tokenize(text)
            #     item_name = text[:is_index].strip()
            #     self.my_mind[item_name] = tokens[-1]
            # self.print_what_i_know()


            # stdout.write('\r%d...' % i)
            # stdout.flush()
            # sleep(1)
            # i += 1
            
            # if i > 100:
            #     break
