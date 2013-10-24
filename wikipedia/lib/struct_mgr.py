from wikipedia.models import *

class StructureManager():
    
    def __init__(self):
        pass

    def add_pvalue(self, prop=None, pv=None, concept=None, amount=None):
        if not prop:
            raise Exception('No property specified')

        if concept:
            pv, created = PropertyValue.objects.get_or_create(
                concept=concept)
        if amount:
            pv, created = PropertyValue.objects.get_or_create(
                amount=amount)

        if not pv.props.filter(pk=prop.id).count():
            pv.props.add(prop)
        
        return prop

    def add_av(self, ass=None, av=None, concept=None, adj=None):
        if not ass:
            raise Exception('No assertion specified')

        if concept:
            av, created = AssertionValue.objects.get_or_create(
                concept=concept)
        if adj:
            av, created = AssertionValue.objects.get_or_create(
                adj=adj)
        
        if not av.assertions.filter(pk=ass.id).count():
            av.assertions.add(ass)

        return ass
