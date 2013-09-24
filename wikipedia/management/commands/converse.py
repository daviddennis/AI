from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection, Assertion, Relation
from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.interpreter import Interpreter
from wikipedia.lib.query_mgr import QueryManager
from wikipedia.lib.nlp_gen import NLPGenerator
from wikipedia.lib.causation import CausationManager
from sys import stdout
from time import sleep
import sys
from text.blob import TextBlob

class Command(BaseCommand):

    computer_mind = {}
    user_mind = {}

    def handle(self, *args, **options):
        interpreter = Interpreter()
        query_mgr = QueryManager()
        nlp_generator =  NLPGenerator()
        causation = CausationManager()

        interpreter.causation = causation

        if 'verbs' in args:
            print 'Loading en...'
            import en

        print '\nHello\n'
        text = ''
        
        while True:
            print '> ',
            text = raw_input().upper()
            if text.lower() in ('bye', 'off', 'later', 'cya', 'end', 'e', 'goodbye', 'exit'):
                break

            # tb = TextBlob(text)
            # tags = tb.tags
            # print tags
            #tags = [('MARY', 'NN'), ('WALK', 'VBD'), ('TO', 'TO'), ('SCHOOL', 'NN')]
            try:
                tags = [(word.upper(), pos_tag) for word, pos_tag in en.sentence.tag(text)]
            except:
                #tags = [('MARY', 'NN'), ('WENT', 'VBD'), ('TO', 'TO'), ('THE', 'DT'), ('ZOO', 'NN')]
                tags = None
            
            sentence = interpreter.parser.remove_parentheses(text)
            sentence = interpreter.parser.space_punctuation(sentence)
            sentence_list = [sentence]
            parsed_sentence = interpreter.parser.parse(sentence_list, tags=tags)

            interpretations = interpreter.interpret(parsed_sentence, thinker=self)

            print '----'*5
            for interpretation in interpretations:
                print interpretation
                if query_mgr.is_query(interpretation):
                    print ':Query'
                    query = query_mgr.construct_query(interpretation)
                    answer = query_mgr.process_query(query)
                    answer_sentence = nlp_generator.deparse(answer)
                    print '\n:: %s\n' % (answer_sentence)
                else:
                    print ':Instruction'
                    interpreter.process_thought(interpretation)
                #self.process_thought(interpretation)

            #self.store_concepts(latest)

            # if query_mgr.is_query(parsed_sentence):
            #     print ':Query'
            #     query = query_mgr.construct_query(parsed_sentence)
            #     answer = query_mgr.process_query(query)
            #     answer_sentence = nlp_generator.deparse(answer)
            #     print '\n:: %s\n' % (answer_sentence)
            # elif causation.is_if_statement(parsed_sentence):
            #     print ':Instruction'
            #     if_stmt = interpreter.process_if(parsed_sentence, causation=causation)
            #     print '\n:: %s\n' % (if_stmt)
            # else:
            #     print ':Instruction'
            #     thought = interpreter.interpret(parsed_sentence, thinker=self)
            #     print thought
                #if thought:
                #    self.add_thought(thought)
                
        print '\nGoodbye.\n'
        return

    
    def add_thought(self, thought):
        self.my_mind[thought[0].name] = thought[1]

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
