
class WordManager():
    
    def __init__(self):
        pass

    def get_root_word(self, item):
        item_name = None
        if isinstance(item, Concept):
            item_name = item.name
        elif isinstance(item, str):
            item_name = item.name

        return item_name
