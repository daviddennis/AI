#from wikipedia.models import Concept, Connection
from conceptnet.models import *
from sys import stdout
from time import sleep


if __name__ == "__main__":
    en = Language.get('en')
    #terms = 'dog mammal animal pet person human'.split(' ')
    terms = 'spaceship computer planet house continent country'.split(' ')
    terms += 'cookie friend cat man woman species hat spanish'.split(' ')
    terms += 'america apartment gun ship pig screen file money'.split(' ')
    terms += 'butt cup penis vagina teeth mouth head body cold'.split(' ')
    terms += 'hand arm leg finger nail stomach waist eye lip'.split(' ')
    assertions = []
    for term in terms:
        assertions += list(Assertion.objects.filter(concept1__text=term).all())
        assertions += list(Assertion.objects.filter(concept2__text=term).all())
    print len(assertions)
    new_file = open('assertions.csv', 'w')
    for i, assertion in enumerate(assertions):
        try:
            new_file.write('%s,%s,%s,%s,%s\n' % (assertion.concept1.text, 
                                                 assertion.relation, 
                                                 assertion.concept2.text,
                                                 assertion.score,
                                                 assertion.frequency.value))

            stdout.write('\rLine %d...' % i)
            stdout.flush()
        except:
            pass
    print '\n'
    #print Assertion.objects.filter(language=en)[0]

