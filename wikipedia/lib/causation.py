from wikipedia.models import Stopword, Assertion, IfStmt, VerbConstruct

class CausationManager():

    def __init__(self):
        pass

    def is_if_statement(self, parsed_sentence):
        first_item = parsed_sentence[0]
        if isinstance(first_item, Stopword):
            if first_item.string.upper() == "if".upper():
                return True
        return False

    def consider_implications(self, assertion):
        if_statements = IfStmt.objects.filter(
            assertion1__id=assertion.id).all()
        if not if_statements:
            abstract_assertion = Assertion.objects.filter(
                concept1__name="SOMETHING",
                relation=assertion.relation,
                concept2=assertion.concept2).all()[0]
            if_statements = IfStmt.objects.filter(
                assertion1__id=abstract_assertion.id).all()        
        for if_statement in if_statements:
            if if_statement.vc2:
                verb_construct, created = VerbConstruct.objects.get_or_create(
                    concept1=assertion.concept1,
                    verb=if_statement.vc2.verb,
                    concept2=if_statement.vc2.concept2)
                print verb_construct
                      
