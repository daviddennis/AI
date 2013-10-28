from wikipedia.models import *
from annoying.functions import get_object_or_None
from django.core.exceptions import MultipleObjectsReturned

class QuestionAsker():

    def __init__(self):
        self.nlp_generator = None
        self.word_mgr = None
        self.query_mgr = None
        self.q_all = Quantifier.objects.get(name="ALL")

    def ask_question(self, items=[]):
        have_question = False
        question_parse = None
        logical_path = []
        q_path = []

        for item in items:
            if isinstance(item, Category):
                logical_path = [item]
                child = item.child
                parent = item.parent

                # Parent-child questions
                verb_constructs = VerbConstruct.objects.filter(concept1=parent).all()
                if verb_constructs:
                    for vc in verb_constructs:
                        # Question to ask
                        hypothetical_vc = VerbConstruct(
                            concept1=child,
                            complex_verb=vc.complex_verb,
                            verb=vc.verb,
                            concept2=vc.concept2)

                        # Check answered
                        if not VerbConstruct.objects.filter(
                            quantifier__in=[self.q_all, None],
                            concept1=child,
                            complex_verb=vc.complex_verb,
                            verb=vc.verb,
                            concept2=vc.concept2).count() and vc.concept2:

                            q_path = [vc]
                            answer = {
                                "type": "question",
                                "sentence": [hypothetical_vc]
                                }
                            question_parse, question_sentence = self.nlp_generator.process_question(answer)
                            question = self.query_mgr.construct_query(question_parse)
                            question['nlp_sentence'] = question_sentence

                            have_question = True


        if not have_question:

            for item in items:
                if isinstance(item, Category):
                    logical_path = [item]
                    child = item.child
                    parent = item.parent

                    categories = Category.objects.filter(child=child).all()
                    if not categories:
                        what_is_a = StopwordSequence.objects.get(string="WHAT IS A")
                        answer = {
                            "type": "question",
                            "sentence": [what_is_a, parent]
                            }
                        #question_parse, question_sentence = self.nlp_generator.process_question(answer)
                        question = self.query_mgr.construct_query(question_parse)
                        question['nlp_sentence'] = question_sentence

                        have_question = True                        


        if have_question:
            question['logical_path'] = logical_path + q_path
            return question

    def answer_question(self, question=None, items=[]):

        if question and items:
            if question.get('type') in self.query_mgr.verify_words:

                for item in items:
                    if isinstance(item, Concept):
                        if item.name == "YES":

                            for sent_item in question.get("sentence", []):
                                if isinstance(sent_item, VerbConstruct):
                                    vc = sent_item
                                    created = False
                                    try:
                                        verb_construct, created = VerbConstruct.objects.get_or_create(
                                            concept1=vc.concept1,
                                            verb=vc.verb,
                                            complex_verb=vc.complex_verb,
                                            concept2=vc.concept2)
                                    except MultipleObjectsReturned:
                                        verb_constructs = VerbConstruct.objects.filter(
                                            concept1=vc.concept1,
                                            verb=vc.verb,
                                            complex_verb=vc.complex_verb,
                                            concept2=vc.concept2).all()
                                        verb_constructs[0].delete()
                                    if created:
                                        print "Added %s" % vc
