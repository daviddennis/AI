from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import Concept, Connection
import urllib2
from BeautifulSoup import BeautifulSoup
from operator import itemgetter
import sys
from annoying.functions import get_object_or_None
import random
from random import randint
#from lxml import etree

class Command(BaseCommand):

    def handle(self, *args, **options):

        # print 'Deleting concepts & connections...'
        # Concept.objects.all().delete()
        # Connection.objects.all().delete()

        print 'Exploring first link...'
        visited_urls = set()

        # url = "http://en.wikipedia.org/wiki/Wall_Street_Journal"
        # next_urls = set([url])
        # while len(next_urls) > 0:
        #     url = list(next_urls)[0]
        #     next_urls.remove(url)
        #     try:
        #         visited_urls.add(url)
        #         sub_links = self.store_page(url)
        #     except:
        #         pass
        #     print sub_links[:20]
        #     for sub_link in sub_links:
        #         if sub_link in visited_urls:
        #             continue
        #         next_urls.add(sub_link)
            
        urls = {
           "http://en.wikipedia.org/wiki/Barack_Obama":20
           }
        while len(urls) > 0:
            #if randint(1, 10) != 10:
            print "Sorting urls..."
            sorted_urls = sorted(urls.iteritems(), key=itemgetter(1), reverse=True)
            print "Done sorting..."
            print sorted_urls[:30]
            url = sorted_urls[0][0]
            #else:
            #    url = random.choice(urls.keys())
            print url
            del urls[url]
            try:
                visited_urls.add(url)
                sub_links = self.store_page(url)
            except:
                pass
            for sub_link in sub_links:
                if sub_link in visited_urls:
                    continue
                urls[sub_link] = urls.get(sub_link, 0) + 1
            # Clean up
            if len(urls) > 20000:
                print 'Cleaning up...'
                lowest_urls = sorted(urls.iteritems(), key=itemgetter(1))[:-20000]
                for low_url, val in lowest_urls:
                    del urls[low_url]

    def store_page(self, url):
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        resp = urllib2.urlopen( req )
        html = resp.read()

        print 'Getting page data...'

        try:
            soup = BeautifulSoup(html)
        except:
            return []

        page_concept_name = [x.contents[0] for x in soup.findAll("h1", { "class":"firstHeading" })][0].text.upper()
        print page_concept_name

        # Check if connections already explored
        existing_concept = get_object_or_None(Concept, name=page_concept_name)
        if existing_concept:
            existing_connections = Connection.objects.filter(conceptA_id=existing_concept.id).all()
            if existing_connections:
                print 'Connections already explored...returning...'
                return []

        page_concept = self.create_or_update_concept(page_concept_name, url)

        page_text_soup = soup.find("div", {"id": "mw-content-text"})
        page_text_soup_tag_list = page_text_soup.findAll("p")
        page_text_soup_tag_list += page_text_soup.findAll("li")

        print 'Reading concept names...'

        concept_names = []
        wiki_links = []
        for tag in page_text_soup_tag_list:
           initial_links = tag.findAll("a")
           links = []
           for link in initial_links:
               try:
                   if '#' not in link['href']:
                       links += [link]
               except:
                   pass
           concept_names += self.extract_link_concepts(links)
           wiki_links += self.extract_outbound_wikilinks(links)
        wiki_links = list(set(wiki_links))

        print 'Storing concept name & connections...'
        
        # Store concepts & connections
        for concept_name in concept_names:
            concept = self.create_or_update_concept(concept_name, url)

            if page_concept.name == concept.name:
                continue

            try:
                existing_connection = Connection.objects.get(
                    conceptA=page_concept,
                    conceptB=concept)

                existing_connection.weight = existing_connection.weight + 1
                existing_connection.save()

            except Connection.DoesNotExist:
                new_connection = Connection(
                    conceptA=page_concept,
                    conceptB=concept,
                    weight=1)
                new_connection.save()

        print 'Returning outbound links...'

        return wiki_links

        #import lxml.html as lh
        #doc=lh.parse(resp)
        #print doc.getroot().find('//*[@id="firstHeading"]/span').text
        #print doc.xpath('//*[@id="firstHeading"]/span')
        
        #lxml_htmlparser = etree.HTMLParser()

        #tree = etree.parse(resp, lxml_htmlparser)
        #print tree.xpath('//*[@id="firstHeading"]/span')

    def extract_link_concepts(self, links):
        concepts = []
        for link in links:
            link_text = link.text
            if link_text in (''):
                continue
            if len(link_text) < 1:
                continue
            if link_text[0] == '[':
                continue
            if link_text[0] == '^':
                continue
            if len(link_text) > 3:
                if link_text[:3] == 'htt':
                    continue
            link_text = link_text.upper().encode('ascii', 'ignore')
            if link_text == "CITATION NEEDED":
                continue
            concepts += [link_text]
        return concepts

    def create_or_update_concept(self, concept_name, url=None):

        try:
            existing_concept = Concept.objects.get(name=concept_name)

            if existing_concept.frequency == None:
                existing_concept.frequency = 0
            existing_concept.frequency = existing_concept.frequency + 1
            existing_concept.stats_status = 'updated'
            existing_concept.save()

            concept = existing_concept
        except Concept.DoesNotExist:
            concept = Concept(
                name=concept_name,
                frequency=1,
                url=url)
            concept.save()

        return concept

    def extract_outbound_wikilinks(self, links):
        wikilinks = []
        for link in links:
            try:
                href = link['href']
                if len(href) < 1:
                    continue
                if 'wiki' not in href:
                    continue
                if href.startswith('/wiki'):
                    href = 'http://en.wikipedia.org' + href
                wikilinks += [href]
            except:
                pass
        return wikilinks
