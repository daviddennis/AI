from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
from wikipedia.lib.parser import Parser
from wikipedia.lib.interpreter import Interpreter
from wikipedia.lib.query_mgr import QueryManager
from wikipedia.lib.nlp_gen import NLPGenerator
from wikipedia.lib.causation import CausationManager
from wikipedia.lib.thought_processor import ThoughtProcessor
from wikipedia.lib.medium_thought_processor import MediumThoughtProcessor
from wikipedia.lib.word_mgr import WordManager
from wikipedia.lib.query_processor import QueryProcessor
from wikipedia.lib.question_asker import QuestionAsker
from wikipedia.lib.struct_mgr import StructureManager
from wikipedia.lib.auto_translate import translations
from sys import stdout
from time import sleep
import sys
from text.blob import TextBlob

class Command(BaseCommand):

    computer_mind = {}
    user_mind = {}

    context = None
    
    def handle(self, *args, **options):
        self.en = None

        self.word_mgr = WordManager()
        interpreter = Interpreter()
        query_mgr = QueryManager()
        query_processor = QueryProcessor()
        nlp_generator =  NLPGenerator()
        causation = CausationManager()
        thought_processor = ThoughtProcessor()
        medium_thought_processor = MediumThoughtProcessor()
        question_asker = QuestionAsker()
        struct_mgr = StructureManager()

        nlp_generator.parser = interpreter.parser
        nlp_generator.word_mgr = self.word_mgr
        interpreter.thought_processor = thought_processor
        interpreter.causation = causation
        thought_processor.struct_mgr = struct_mgr
        question_asker.nlp_generator = nlp_generator
        question_asker.word_mgr = self.word_mgr
        question_asker.query_mgr = query_mgr

        learned_items = set()
        prev_question = None
        shortest_interpretations = []
        self.seen = set()

        no_en = False
        if 'noverbs' in args:
            no_en = True

        print '\nHello\n'
        text = ''

        while True:
            print '> ',
            text = raw_input().upper()
            if text.lower() in ('bye', 'off', 'later', 'cya', 'end', 'e', 'goodbye', 'exit'):
                break

            if not self.en and not no_en:
                import en
                self.en = en

            if self.en:
                tags = [(word.upper(), pos_tag) for word, pos_tag in self.en.sentence.tag(text)]
                print tags
            else:
                tags = None
            
            sentence = interpreter.parser.remove_parentheses(text)
            sentence = interpreter.parser.space_punctuation(sentence)
            sentence = self.run_auto_translate(sentence)
            sentence_list = [sentence]
            parsed_sentence = interpreter.parser.parse(sentence_list, tags=tags)

            interpretations = interpreter.interpret(parsed_sentence, thinker=self)
            interpreter.clear_interpretations()

            if interpreter.one_item:
                print interpreter.one_item

            num_interpretations = len(interpretations)
            print '# interpretations: %s' % num_interpretations
            
            for x in interpretations[:100]:
                shortest_interpretations += [x]
                print x

            if interpretations:
                print '----'*5 + ' FIRST LEVEL'
            thoughts = []
            for interpretation in interpretations:
                thought_processor.process_thought(interpretation, thinker=self)
                thoughts += thought_processor.get_interpretations()
                thought_processor.clear_interpretations()

            for key, val in thought_processor.learned.iteritems():
                print key,':',val
            #print thought_processor.learned.values()
            learned_items |= set([x for y in thought_processor.learned.values() for x in y])
            thought_processor.learned = {}

            if thoughts:
                print '----'*5 + ' SECOND LEVEL'
                for thought in thoughts[:100]:
                    #if isinstance(thought[0], Category):
                    print thought
                medium_thoughts = []
                for thought in thoughts:
                    medium_thought_processor.process_thought(thought, thinker=self)
                    medium_thoughts += medium_thought_processor.interpretations
                    medium_thought_processor.interpretations = []
                if medium_thoughts:
                    print '----'*5 + ' THIRD LEVEL'
                    for x in medium_thoughts[:100]:
                        print x

                print '----'*5
                for key, val in medium_thought_processor.learned.iteritems():
                    print key,':',val
                learned_items |= set([x for y in thought_processor.learned.values() for x in y])
                medium_thought_processor.learned = {}

                shortest_interpretations += thoughts

            print '\n\n'

            # Question Analysis
            for potential_question in interpretations + thoughts:
                query_processor.process_thought(potential_question)
            if query_processor.learned:
                print '----'*5 + ' QUESTION ANALYSIS LEVEL'
                for key, val in query_processor.learned.iteritems():
                    print key,':',val
            query_processor.learned = {}

            print '\n'

            #for x in sorted(shortest_interpretations, key=len)[:10]:
            #    print x
            #shortest_interpretations = []

            #print '\n\n'

            #print learned_items
            #print '{'
            #for x,y in self.computer_mind.iteritems():
            #    print x,':',y
            #print '}'
            self.seen = set()

            # Answer Question
            if prev_question:
                question_asker.answer_question(question=prev_question, items=learned_items)
                prev_question = None

            # Ask Question
            prev_question = question_asker.ask_question(items=learned_items)
            if prev_question:
                for item in prev_question.get('logical_path', []):
                    print item
                print prev_question.get('nlp_sentence')

            learned_items = set()

            print '\n\n'

            #self.store_concepts(latest)
                
        print '\nGoodbye.\n'
        return
            # tb = TextBlob(text)
            # tags = tb.tags
            # print tags
            #tags = [('MARY', 'NN'), ('WALK', 'VBD'), ('TO', 'TO'), ('SCHOOL', 'NN')]
            #try:
            #except:
                #tags = [('MARY', 'NN'), ('WENT', 'VBD'), ('TO', 'TO'), ('THE', 'DT'), ('ZOO', 'NN')]
                #tags = None
    #print interpretation
    # if query_mgr.is_query(interpretation):
    #     print ':Query'
    #     query = query_mgr.construct_query(interpretation)
    #     answer = query_mgr.process_query(query)
    #     answer_sentence = nlp_generator.deparse(answer)
    #     print '\n:: %s\n' % (answer_sentence)
    # else:
    #print ':Instruction'


    def remember(self, item, key=None):
        if len(self.computer_mind) > 2000:
            return

        val = item

        keys = []
        if key:
            keys += [key]

        if isinstance(item, Concept):
            keys += [item.name]
            if self.word_mgr._is(item, "MALE"):
                keys += ["HE"]
            else:
                if self.word_mgr._is(item, "FEMALE"):
                    keys += ["SHE"]
                else:
                    keys += ["IT"]
        elif isinstance(item, Amount):
            keys += [item.concept.name]
            keys += ["AMOUNT"]
            keys += ["THEM"]
        elif isinstance(item, List):
            keys += [item.type.name]
            keys += ["LIST"]
            keys += ["THEM"]
        elif isinstance(item, Group):
            keys += [item.child_concept.name]
            keys += ["GROUP"]
        elif isinstance(item, Property):
            if item.key_concept:
                keys += [item.key_concept.name]

        for key in keys:
            if key not in self.seen:
                self.computer_mind[key] = val
                self.seen |= set([key])


    def recall(self, item):
        if isinstance(item, Stopword):
            return self.computer_mind.get(item.name)
        if isinstance(item, Concept):
            recalled_item = self.computer_mind.get(item.name)
            if recalled_item:
                return recalled_item
            
        #    for word_form in self.word_mgr.get_forms(item):
        #        #print word_form
        #        recalled_item = self.computer_mind.get(word_form)
        #        if recalled_item:
        #            return recalled_item
    
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


    def run_auto_translate(self, sentence):
        before = sentence
        for key, val in translations.iteritems():
            _in = key.upper()
            _out = val.upper()
            if _in in sentence:
                sentence = sentence.replace(_in, _out)

        if before != sentence:
            print "\nTranslations:"
            print '%s -> %s\n' % (before, sentence)

        return sentence

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
