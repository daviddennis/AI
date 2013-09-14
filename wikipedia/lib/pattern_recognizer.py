from wikipedia.models import Concept, Connection, StopwordSequence
from wikipedia.lib.parser import Stopword

class PatternRecognizer():
    
    def __init__(self):
        pass

    def recognize(self, item_list, pattern):
        args = pattern.split(' ')
        for i, arg in enumerate(args):
            arg = arg.strip()
            item = item_list[i]
            if arg.upper() == "CONCEPT":
                if not isinstance(item, Concept):
                    return False
            if arg.upper() == "SWS":
                if not isinstance(item, StopwordSequence):
                    return False
            if arg.upper() == "SW":
                if not isinstance(item, Stopword):
                    return False
        return True
