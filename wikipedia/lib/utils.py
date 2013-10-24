from django.db.models.signals import pre_save
from functools import wraps
from django.core.exceptions import MultipleObjectsReturned
import sys

def autoconnect_to_signals(cls):
    """ 
    Class decorator that automatically connects pre_save / post_save signals on 
    a model class to its pre_save() / post_save() methods.
    """
    def connect(signal, func):
        cls.func = staticmethod(func)
        @wraps(func)
        def wrapper(sender, **kwargs):
            return func(kwargs.get('instance'))
        signal.connect(wrapper, sender=cls)
        return wrapper

    if hasattr(cls, 'pre_save'):
        cls.pre_save = connect(pre_save, cls.pre_save)

    if hasattr(cls, 'post_save'):
        cls.post_save = connect(post_save, cls.post_save)
    
    return cls


def get_or_create_or_delete(cls, **kwargs):
    obj = None
    created = False
    try:
        obj, created = cls.objects.get_or_create(**kwargs)
    except MultipleObjectsReturned:
        print 'MultipleObjectsReturned!!!'
        all_cls = cls.objects.filter(**kwargs).all()
        if all_cls:
            if len(all_cls) > 1:
                obj = all_cls[1]
                all_cls[0].delete()
                print 'Deleted 1 %s' % cls.__name__
    
    return obj, created
