from django.core.management.base import BaseCommand, CommandError
from wikipedia.models import *
import urllib2

class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'http://rtw.ml.cmu.edu/rtw/kbbrowser/list.php?pred=country'
        #url = args[0]

        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        resp = urllib2.urlopen( req )
        html = resp.read()

        #f = open('tmp.txt','w')
        #f.write(html)
        #f.close()
        
