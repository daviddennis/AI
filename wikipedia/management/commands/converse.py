from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
from wikipedia.lib.parser import Parser, Stopword
from wikipedia.lib.interpreter import Interpreter
from wikipedia.lib.query_mgr import QueryManager
from wikipedia.lib.nlp_gen import NLPGenerator
from wikipedia.lib.causation import CausationManager
from wikipedia.lib.thought_processor import ThoughtProcessor
from wikipedia.lib.word_mgr import WordManager
from sys import stdout
from time import sleep
import sys
from text.blob import TextBlob

class Command(BaseCommand):

    computer_mind = {}
    user_mind = {}

    context = None

    def handle(self, *args, **options):
        self.word_mgr = WordManager()
        interpreter = Interpreter()
        query_mgr = QueryManager()
        nlp_generator =  NLPGenerator()
        causation = CausationManager()
        thought_processor = ThoughtProcessor()
        interpreter.thought_processor = thought_processor
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
            interpreter.clear_interpretations()

            print interpreter.one_item

            num_interpretations = len(interpretations)
            print '# interpretations: %s' % num_interpretations
            
            if num_interpretations < 30:
                print interpretations

            print '----'*5
            for interpretation in interpretations:
                #print interpretation
                if query_mgr.is_query(interpretation):
                    print ':Query'
                    query = query_mgr.construct_query(interpretation)
                    answer = query_mgr.process_query(query)
                    answer_sentence = nlp_generator.deparse(answer)
                    print '\n:: %s\n' % (answer_sentence)
                else:
                    #print ':Instruction'
                    thought_processor.process_thought(interpretation, thinker=self)
                #self.process_thought(interpretation)

            print thought_processor.learned
            thought_processor.learned = {}

            #self.store_concepts(latest)
                
        print '\nGoodbye.\n'
        return

    def remember(self, item):
        if isinstance(item, Concept):
            self.computer_mind[item.name] = item
        elif isinstance(item, Amount):
            self.computer_mind[item.concept.name] = item
        elif isinstance(item, List):
            self.computer_mind[item.type.name] = item

    def recall(self, item):
        if isinstance(item, Concept):
            for word_form in self.word_mgr.get_forms(item):
                #print word_form
                recalled_item = self.computer_mind.get(word_form)
                if recalled_item:
                    return recalled_item
        #elif isinstance
    
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
