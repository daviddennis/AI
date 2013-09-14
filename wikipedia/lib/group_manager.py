from wikipedia.models import Concept, Connection, Group, GroupInstance
from annoying.functions import get_object_or_None
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()

class GroupManager():
    
    def __init__(self):
        Group.objects.all().delete()
        GroupInstance.objects.all().delete()
        #pass

    def check_and_form_group(self, parent_concept, child_concept):
        original_parent_concept = parent_concept
        original_child_concept = child_concept
        if parent_concept.category:
            parent_concept = parent_concept.category
        if child_concept.category:
            child_concept = child_concept.category

        parent_is_category = False
        child_is_category = False
        if Concept.objects.filter(category=parent_concept).all():
            parent_is_category = True
        if Concept.objects.filter(category=child_concept).all():
            child_is_category = True

        groups = Group.objects.filter(parent_concept=parent_concept, child_concept=child_concept).all()
        if groups:
            group = groups[0]

            if group.parent_concept == original_parent_concept.category and \
                    group.child_concept == original_child_concept.category:
                group_instance, created = GroupInstance.objects.get_or_create(
                    group=group,
                    parent_concept=original_parent_concept,
                    child_concept=original_child_concept)
                if created:
                    print group_instance
                return created
        else:
            if parent_is_category and child_is_category:
                return self.form_group(parent_concept, child_concept)
        
        return False

    def form_group(self, parent_concept, child_concept):
        parent_concept = self.get_singular_concept(parent_concept)
        child_concept = self.get_singular_concept(child_concept)
        group, created = Group.objects.get_or_create(
            parent_concept=parent_concept,
            child_concept=child_concept)
        if created:
            print group
        return created

    def get_singular_concept(self, concept):
        concept_or_none = get_object_or_None(Concept, name=lmtzr.lemmatize(concept.name.lower()))
        if concept_or_none:
            return concept_or_none
        else:
            return concept
