from wikipedia.models import Concept, Connection, StopwordSequence, Verb, Assertion, VerbConstruct, List, Adjective
from wikipedia.lib.parser import Stopword

class PatternRecognizer():
    
    def __init__(self):
        pass

    def recognize(self, item_list, pattern):
        #keep_looking = False
        args = pattern.split(' ')
        for i, arg in enumerate(args):
            arg = arg.strip()
            if i >= len(item_list):
                if args[i:]:
                    return False
                else:
                    break
            item = item_list[i]
            # if '|' in arg:
            #     if item.__class__.__name__ not in arg.split('|'):
            #         print item.__class__.__name__,arg.split('|')
            #         return False
            arg = arg.upper()
            #keep_looking = False
            if arg.startswith("STRING"):
                if not isinstance(item, str):
                    return False
                continue
            if arg in ("VERB","VERB:"):
                if isinstance(item, Verb):
                    if ':' in arg:
                        if item.name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg.startswith("CONCEPT"):
                if isinstance(item, Concept):
                    if ':' in arg:
                        if item.name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg.startswith("SWS"):
                if isinstance(item, StopwordSequence):
                    if ':' in arg:
                        if item.string != ' '.join(arg.split(':')[1].split('_')):
                            return False
                else:
                    return False
                continue
            if arg.startswith("SW"):
                if isinstance(item, Stopword):
                    if ':' in arg:
                        if item.name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg.startswith("ADJECTIVE"):
                if isinstance(item, Adjective):
                    if ':' in arg:
                        if item.name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg.startswith("LIST"):
                if not isinstance(item, List):
                    return False
            if arg.startswith("ASSERTION"):
                if not isinstance(item, Assertion):
                    return False
            if arg.startswith("VERBCONSTRUCT"):
                if not isinstance(item, VerbConstruct):
                    return False
            if arg == "...":
                continue
        # if keep_looking:
        #     return False
        return True
