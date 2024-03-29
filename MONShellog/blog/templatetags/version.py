from django.template import Library
from MONShellog import settings

register = Library()
VERSION = getattr(settings,'VERSION','unknown')

@register.simple_tag
def get_version():
    """
    Returns the version as a human-format string.
    """
    v = '.'.join([str(i) for i in VERSION[:-1]])
    if VERSION[-1]: 	   
        v = '%s %s' % (v, VERSION[-1])
    return v

