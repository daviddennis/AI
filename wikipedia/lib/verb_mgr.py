
class VerbManager():
    
    def __init__(self):
        pass

    def get_form_name(self, verb, _type=None):

        form_name = verb.name

        if not _type:
            return verb.name
        elif _type == "past":
            form_name = verb.past_name
        elif _type == "participle":
            form_name = verb.participle_name
        elif _type == "s":
            form_name = verb.s_form

        return form_name
