from wikipedia.models import *
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
            if arg == "VERB" or arg.startswith("VERB:"):
                if isinstance(item, Verb):
                    if ':' in arg:
                        if item.name != arg.split(':')[1] and item.past_name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg.startswith("CONCEPT"):
                if isinstance(item, Concept):
                    if ':' in arg:
                        if '_' in item.name:
                            if item.name != ' '.join(arg.split(':')[1].split('_')):
                                return False
                        else:
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
            if arg.startswith("PUNC"):
                if isinstance(item, Punctuation):
                    if ':' in arg:
                        if item.name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg.startswith("NUMBER"):
                if isinstance(item, Number):
                    if ':' in arg:
                        if item.name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg in ("PREP", "PREPOSITION") or arg.startswith("PREP:"):
                if isinstance(item, Preposition):
                    if ':' in arg:
                        if item.name != arg.split(':')[1]:
                            return False
                else:
                    return False
                continue
            if arg.startswith("TIME"):
                if not isinstance(item, Time):
                    return False
            if arg.startswith("AMOUNT"):
                if not isinstance(item, Amount):
                    return False
            if arg.startswith("LIST"):
                if not isinstance(item, List):
                    return False
            if arg.startswith("ASSERTION"):
                if not isinstance(item, Assertion):
                    return False
            if arg.startswith("VERBCONSTRUCT"):
                if not isinstance(item, VerbConstruct):
                    return False
            if arg.startswith("CATEGORY"):
                if not isinstance(item, Category):
                    return False
            if arg.startswith("GROUP"):
                if not isinstance(item, Group):
                    return False
            if arg.startswith("CVERB"):
                if not isinstance(item, ComplexVerb):
                    return False
            if arg.startswith("PROP"):
                if not isinstance(item, Property):
                    return False
            if arg == "...":
                continue
        # if keep_looking:
        #     return False
        return True
