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
        # action is a genre : movies have genres
        
        # ca(child -> c1) : ca(head -> parent), (parent -> [c1])
        ## american is a nationality : composer is a person, person have nationality

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
            else:

                # look at head's parents (composer is a person)
                head_parent_concepts = [ca.parent for ca in head.category_set.all()]
                for parent in head_parent_concepts:

                    groups = Group.objects.filter(
                        parent_concept=parent,
                        child_concept__in=child_category_concepts).all() # person -> [nationality, ...]

                    if groups:
                        group = groups[0]

                        #new_group, created = Group.objects.get_or_create(
                        #    parent_concept=head,
                        #    child_concept=group.child_concept)

                        group_instance, created = GroupInstance.objects.get_or_create(
                            group=group,
                            parent_concept=head,
                            child_concept=child)
                        return group_instance
                    

        return None
        

    def new_vc(self, vc):
        vc2, created = VerbConstruct.objects.get_or_create(
            concept1=vc.concept1,
            amount1=vc.amount1,
            verb=vc.verb,
            complex_verb=vc.complex_verb,
            concept2=vc.concept2,
            amount2=vc.amount2,
            assertion2=vc.assertion2,
            question_fragment2=vc.question_fragment2,
            verb_construct2=vc.verb_construct2,
            property2=vc.property2)
        return vc2
        
        
    def copy(self, cls, instance, add={}):

        kwargs = instance.__dict__

        for key, val in kwargs.items():
            if key.startswith('_'):
                del kwargs[key]
        del kwargs['id']

        kwargs.update(add)

        new_instance, created = cls.objects.get_or_create(**kwargs)

        return new_instance
