
vowels = set('a e i o u'.split(' ') + [x.upper() for x in 'a e i o u'.split(' ')])

gw1 = set("set group bunch lot stack class band club company crowd gang organization".upper().split(' '))
gw2 = set("party society troop accumulation assortment batch bevy bundle clique cluster".upper().split(' '))
gw3 = set("collection conglomerate congregation coterie crew formation gathering mess".upper().split(' '))
gw4 = set("pack platoon posse pool suite".upper().split(' '))

group_words = gw1 | gw2 | gw3 | gw4
