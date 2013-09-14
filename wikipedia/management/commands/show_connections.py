from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection
from django.db.models import Q
from annoying.functions import get_object_or_None
from operator import itemgetter
import sys
from collections import OrderedDict

class Command(BaseCommand):

    def handle(self, *args, **options):
        args = [x.upper() for x in args]
        search_term = None
        search_terms = None
        if len(args) > 0:
            if '-' in args:
                bar_pos = args.index('-')
                search_terms = [' '.join(args[:bar_pos]), ' '.join(args[bar_pos+1:])]
            else:
                search_term = ' '.join(args)

        if search_terms:
            #self.show_similar_connections(search_terms)
            self.get_network_from_concepts(search_terms)
            return

        if search_term:
            self.show_forward_connections(search_term)
        else:
            self.show_combined_connections()            

    def get_network_from_concepts(self, search_terms):
        term1 = search_terms[0]
        term2 = search_terms[1]
        
        middle_concepts_odict = self.get_middle_connections(term1, term2)
        print list(middle_concepts_odict)
        
        net_rank = {}
        for middle_concept in list(middle_concepts_odict)[:25]:
            print middle_concept
            a_odict = self.get_middle_connections(term1, middle_concept)
            b_odict = self.get_middle_connections(middle_concept, term2)

            for key, val in a_odict.iteritems():
                net_rank[key] = net_rank.get(key, 0) + a_odict.get(key, 0)
            for key, val in b_odict.iteritems():
                net_rank[key] = net_rank.get(key, 0) + b_odict.get(key, 0)

            #both_set = set([x for x in a_dict if x in b_dict] + [x for x in b_list if x in a_list])

            #for name in both_set:
            #    net_rank[name] = net_rank.get(name, 0) + a_odict.get(name, 1) * b_odict.get(name, 1)

            print sorted(net_rank.iteritems(), key=itemgetter(1), reverse=True)[:100]
            
            # a_list = list(self.get_middle_connections(term1, middle_concept))[:10]
            # b_list = list(self.get_middle_connections(middle_concept, term2))[:10]
            # net_set |= set([x for x in a_list if x in b_list])
            # net_set |= set([x for x in b_list if x in a_list])
            # print net_set
            
        #print net_set
        #print [x[0] for x in middle_concepts_odict]

    def get_middle_connections(self, term1, term2):

        concept1 = Concept.objects.filter(name=term1).all()[0]
        concept2 = Concept.objects.filter(name=term2).all()[0]
        
        forward_connections = concept1.concept_a_set.all()
        backward_connections = concept2.concept_a_set.all()

        back_concepts_conns = {conn.conceptB.name:conn for conn in backward_connections}

        middle_concepts = []
        for forward_conn in forward_connections:
            concept_name = forward_conn.conceptB.name
            if concept_name in back_concepts_conns:
                back_conn = back_concepts_conns[concept_name] 
                middle_concepts += [(concept_name, forward_conn.weight*back_conn.weight)]
         
        middle_concepts_dict = OrderedDict(sorted(middle_concepts, key=itemgetter(1), reverse=True))
        return middle_concepts_dict

    def show_combined_connections(self):
        connections = Connection.objects.order_by('-weight').all()[:2000]

        conn_dict = {}
        for connection in connections:
            reverse_connections = Connection.objects.filter(conceptA=connection.conceptB, conceptB=connection.conceptA).all()[:1]
            if reverse_connections:
                reverse_connection = reverse_connections[0]
                combined_weight = connection.weight * reverse_connection.weight
                conn_dict[tuple(sorted([connection.conceptA.name, connection.conceptB.name]))] = combined_weight
                #print '%s: %s <-> %s' % (combined_weight, connection.conceptA, connection.conceptB)

        for item, weight in sorted(conn_dict.iteritems(), key=itemgetter(1), reverse=True):
            print weight, ':', item

    def show_forward_connections(self, search_term):
        if search_term:
            try:
                conceptB = Concept.objects.filter(name=search_term.upper()).all()[0]
                print conceptB.id
            except:
                print 'No concept found'
                return
            conceptAs = conceptB.concept_a_set.order_by('-weight').all()[:20]
            if conceptB and len(conceptAs) == 0:
                print 'Concept found but no outbound connections found'
            for concept in conceptAs:
                print concept
            conceptA = conceptB
            conceptBs = conceptA.concept_b_set.order_by('-weight').all()[:20]
            if len(conceptBs) == 0:
                print 'No inbound connections found'
            for concept in conceptBs:
                print concept
        else:
            connections = Connection.objects.order_by('-weight').all()[:100]

            for connection in connections:
                if connection.conceptA.name != "CITATION NEEDED" and connection.conceptB.name != "CITATION NEEDED":
                    print connection
                    
