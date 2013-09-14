from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection, Group, GroupInstance
from annoying.functions import get_object_or_None

class Command(BaseCommand):

    def handle(self, *args, **options):

        concepts_with_categories = Concept.objects.filter(category__isnull=False).all()
        for concept in concepts_with_categories:
            group_or_none = concept.category.abstract_parent_set.all()[:1]
            if group_or_none:
                group = group_or_none[0]
                child_concept = get_object_or_None(Concept, category=group.child_concept)
                if child_concept:
                    group_instance, created = GroupInstance.objects.get_or_create(
                        group=group,
                        parent_concept=concept,
                        child_concept=child_concept)
                    group_instance.save()
                    print group_instance

        return
