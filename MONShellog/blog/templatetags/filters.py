from django import template
from django.template.defaultfilters import striptags
from django.utils.encoding import force_unicode
register = template.Library()

@register.filter
def truncatelen(value,length = 40):
    str=striptags(value)
    str.replace('&nbsp;',' ')
    str.replace('&lt;','<')
    str.replace('&amp;','&')
    str.replace('&quot;','"')
    str.replace('&lt;','<')
    str = force_unicode(str)
    string = ''   
    index = 0
    len = int(length)
    while len > 0:
        char = str[index:index+1]
        index += 1
        if char > u'\x80':
            len -= 2
        else:
            len -= 1
        string += char
    if string != str:
        string += '...'
    return string

