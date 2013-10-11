from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
import urllib2
from BeautifulSoup import BeautifulSoup
from operator import itemgetter
import sys
from annoying.functions import get_object_or_None
import random
from random import randint
from time import sleep

class Command(BaseCommand):

    def handle(self, *args, **options):
        wiki_links = [args[0]]

        file_name = '/root/research/concept_map/wikipedia/management/commands/wiki_sents.txt'
        self.out_file = open(file_name, 'w')

        visited = set()

        for link in wiki_links:
            try:
                if link not in visited:
                    more_links = set(self.read_link(link))
                    #print more_links
                    visited.add(link)
                    for new_link in more_links:
                        if new_link not in visited:
                            wiki_links += [new_link]
            except:
                print 'Warning: %s' % link
                pass
            #sleep(1)

            self.out_file.close()
            self.out_file = open(file_name, 'a')

        return

    def read_link(self, url):
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        resp = urllib2.urlopen( req )
        html = resp.read()
        
        soup = BeautifulSoup(html)        

        page_concept_name = [x.contents[0] for x in soup.findAll("h1", { "class":"firstHeading" })][0].text.upper()
        
        print page_concept_name.upper()
        #print '\n'

        page_concept = get_object_or_None(Concept, name=page_concept_name)

        page_text_soup = soup.find("div", {"id": "mw-content-text"})
        page_text_soup_tag_list = page_text_soup.findAll("p")
        #page_text_soup_tag_list += page_text_soup.findAll("li")

        wiki_links = self.get_outbound_links(page_text_soup_tag_list)

        first_paragraph = ''.join(page_text_soup_tag_list[0].findAll(text=True))
        
        first_sentence = first_paragraph.split('. ')[0]
        #print first_sentence
        #print '-------------'

        try:
            if len(first_sentence) < 250 and len(first_sentence) > 10:
                import string
                first_sentence = filter(lambda x: x in string.printable, first_sentence)
                self.out_file.write(page_concept_name.upper() + '\n')
                self.out_file.write(first_sentence + '\n\n')
        except:
            pass

        return wiki_links


    def get_outbound_links(self, page_text_soup_tag_list):
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
           #concept_names += self.extract_link_concepts(links)
           wiki_links += self.extract_outbound_wikilinks(links)
        wiki_links = list(set(wiki_links))

        return wiki_links

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
                    href = 'http://simple.wikipedia.org' + href
                wikilinks += [href]
            except:
                pass
        return wikilinks
