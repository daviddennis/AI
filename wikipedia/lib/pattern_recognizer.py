from wikipedia.models import Concept, Connection, StopwordSequence, Verb
from wikipedia.lib.parser import Stopword

class PatternRecognizer():
    
    def __init__(self):
        pass

    def recognize(self, item_list, pattern):
        args = pattern.split(' ')
        for i, arg in enumerate(args):
            arg = arg.strip().upper()
            item = item_list[i]
            if arg.startswith("STRING"):
                if not isinstance(item, str):
                    return False
                continue
            if arg.startswith("VERB"):
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
                if not isinstance(item, StopwordSequence):
                    return False
                continue
            if arg.startswith("SW"):
                if not isinstance(item, Stopword):
                    return False
                continue
        return True
