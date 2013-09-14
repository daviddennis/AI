from wikipedia.models import StopwordSequence, Concept, Assertion

class NLPGenerator():
    
    def __init__(self):
        pass

    def deparse(self, thought_parse):
        tokens = ['I','do','not','understand']

        if thought_parse['type'] == 'definition':
            tokens = self.process_definition(thought_parse)
        if thought_parse['type'] == 'verification':
            tokens = self.process_verification(thought_parse)
        
        sentence = self.make_sentence(tokens)
        return sentence

    def process_definition(self, thought_parse):
        tokens = []

        for item in thought_parse['sentence']:
            if isinstance(item, Assertion):
                if item.relation.name == "IsA":
                    link_words = ['is','a']
                tokens += ['A'] + [item.concept1.name] + link_words + [item.concept2.name]
                
        return tokens

    def process_verification(self, thought_parse):
        tokens = []

        for item in thought_parse['sentence']:
            if isinstance(item, str):
                tokens += [item]

        return tokens

    def make_sentence(self, tokens):
        sentence = ''

        num_tokens = len(tokens)
        for i, token in enumerate(tokens):
            if i == 0:
                sentence += token.capitalize()
            else:
                sentence += token.lower()
            
            if i < num_tokens-1:
                sentence += ' '
            else:
                sentence += '.'
            
        return sentence
