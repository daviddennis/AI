from wikipedia.models import *

class PatternRecognizer():
    
    def __init__(self):
        self.model_dict = {
            "STRING": str,
            "VERB": Verb,
            "CONCEPT": Concept,
            "SWS": StopwordSequence,
            "ADJ": Adjective,
            "ADJECTIVE": Adjective,
            "SW": Stopword,
            "PUNC": Punctuation,
            "PUNCTUATION": Punctuation,
            "NUMBER": Number,
            "PREP": Preposition,
            "PREPOSITION": Preposition,
            "TIME": Time,
            "AMOUNT": Amount,
            "LIST": List,
            "ASSERTION": Assertion,
            "VERBCONSTRUCT": VerbConstruct,
            "CATEGORY": Category,
            "GROUP": Group,
            "CVERB": ComplexVerb,
            "PROP": Property,
            "PROPERTY": Property,
            "NAME": PersonName,
            "CPREP": PrepConstruct,
            "MONEY": Money,
            "QUANTIFIER": Quantifier,
            "Q": Quantifier,
            "ALIAS": Alias,
            "GI": GroupInstance,
            "QFRAG": QuestionFragment,
            "PREPCONSTRUCT": PrepConstruct,
            "PC": PrepConstruct,
            "ADVERB": Adverb
            }
        self.patterns = set()

    def recognize(self, item_list, pattern):

        # if pattern in self.patterns:
        #     raise Exception("Redundant pattern: %s" % pattern)
        # else:
        #     self.patterns.add(pattern)

        args = pattern.split(' ')
        for i, arg in enumerate(args):
            arg = arg.strip().upper()
            if i >= len(item_list):
                if args[i:]:
                    return False
            item = item_list[i]

            if arg == "...":
                continue

            if '|' in arg:

                sub_args = arg.split('|')
                matched = False
                for sub_arg in sub_args:
                    cls = self.model_dict.get(sub_arg)
                    if cls:
                        if isinstance(item, cls):
                            matched = True
                            break
                if not matched:
                    return False

            else:

                if ':' in arg:
                    cls = self.model_dict.get(arg.split(':')[0])
                else:
                    cls = self.model_dict.get(arg)
                if cls:
                    if isinstance(item, cls):
                        if ':' in arg:
                            try:
                                item_name = item.name
                            except:
                                item_name = item.string
                            if item_name != ' '.join(arg.split(':')[1].split('_')):
                                return False
                    else:
                        return False
                else:
                    raise Exception('Unknown model %s' % arg)
        
        return True

                # for model_name in self.model_dict:
                #     if arg.startswith(model_name):
                #         cls = self.model_dict[model_name]
                #         if isinstance(item, cls):
                #             if ':' in arg:
                #                 try:
                #                     item_name = item.name
                #                 except:
                #                     item_name = item.string
                #                 if item_name != arg.split(':')[1]:
                #                     return False
                #         else:
                #             return False


                                # if ':' in arg:
                                #     try:
                                #         item_name = item.name
                                #     except:
                                #         item_name = item.string
                                #     if item_name == ' '.join(sub_arg.split(':')[1].split('_'))::
                                #         num_matched += 1
            

    def old_recognize(self, item_list, pattern):
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
            if arg.startswith("ADJ"):
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
            if arg.startswith("NAME"):
                if not isinstance(item, PersonName):
                    return False
            if arg.startswith("CPREP"):
                if not isinstance(item, PrepConstruct):
                    return False
            if arg.startswith("MONEY"):
                if not isinstance(item, Money):
                    return False
            if arg in ("Q", "QUANTIFIER"):
                if not isinstance(item, Quantifier):
                    return False
            if arg == "...":
                continue
        # if keep_looking:
        #     return False
        return True
