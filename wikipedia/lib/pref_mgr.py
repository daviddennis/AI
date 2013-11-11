
class PreferenceManager():

    def __init__(self):
        pass

    def filter_preferred(self, thought_dict):
        for key, val in thought_dict.iteritems():
            if key == 'propertys':
                new_props = []
                for prop in val:
                    
