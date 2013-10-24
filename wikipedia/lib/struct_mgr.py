from wikipedia.models import *

class StructureManager():
    
    def __init__(self):
        pass

    def add_pvalue(self, prop=None, pv=None, concept=None, amount=None):
        if not prop:
            return

        if concept:
            pv, created = PropertyValue.objects.get_or_create(
                concept=concept)
        if amount:
            pv, created = PropertyValue.objects.get_or_create(
                amount=amount)

        if not pv.props.filter(pk=prop.id).count():
            pv.props.add(prop)
        
        return prop
