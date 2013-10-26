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


    def cc_group_instance(self, child=None, head=None):

        if not isinstance(child, Concept) or not isinstance(head, Concept):
            return None
        
        # ca(child -> c1) : (head -> [c1])

        child_category_concepts = [ca.parent for ca in child.category_set.all()]
        if child_category_concepts:
            groups = Group.objects.filter(
                parent_concept=head,
                child_concept__in=child_category_concepts).all()
            if groups:
                group = groups[0]
                group_instance, created = GroupInstance.objects.get_or_create(
                    group=group,
                    parent_concept=head,
                    child_concept=child)
                return group_instance

        return None
        
        
