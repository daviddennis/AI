from wikipedia.lib.quick_lists import vowels


def a_form(first_word, caps=None):
    a = None
    if first_word[0] in vowels:
        a = 'an'
    else:
        a = 'a'
    
    if caps:
        return a.upper()
    else:
        return a
