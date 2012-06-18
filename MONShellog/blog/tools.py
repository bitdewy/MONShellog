from blog.models import Entry
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import InvalidPage, EmptyPage
from django.utils.dateformat import format
import urllib, hashlib

MAX_WEIGHT = 4

def render_to(tmpl):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            return render_to_response(tmpl, output,
                                      context_instance=RequestContext(request))
        return wrapper
    return renderer

class Archive:
  link = ''
  title = ''

def page(obj,page_id):
    try:
        o = obj.page(page_id)
    except(EmptyPage):
        o = obj.page(1)
    return o

def get_page_id(page):
    try:
        id = int(page)
    except(ValueError):
        return 1
    return id

def set_all_image(list,size):
    default = "http://item.slide.com/r/1/53/i/PW0NiYur5T-voxkcv5lWmEIH2qgKY7vA/"
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    floor = 1
    for one in list:
        gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(one.email).hexdigest(), 'default':default, 'size':size})
        one.image = gravatar_url
        one.floor = floor
        floor += 1
    return list 

def get_archive():    
    categories = []
    tags = []
    archive = []
    entries = Entry.objects.filter(status__exact = 'publish').order_by('-pub_date')
    months = entries.dates('pub_date','month',order='DESC')
    for mon in months:
        m = Archive()
        m.link = "/archive/" + format(mon,'Y/m') + "/"
        m.title = format(mon,'b,Y')
        archive.append(m)
    for entry in entries:
        if entry.category not in categories:
            categories.append(entry.category)    
        t = entry.tags.all()
        for tag in t:
            if tag not in tags:
                tags.append(tag)  
    if tags:
        min_count = max_count = tags[0].count
        for tag in tags:
            if tag.count < min_count:
                min_count = tag.count
            if max_count < tag.count:
                max_count = tag.count
        range = float(max_count - min_count)
        if range == 0.0:
            range = 1.0
        for tag in tags:
            tag.weight = int(MAX_WEIGHT * (tag.count - min_count) / range)    
    return {'entries':entries,'categories':categories,'tags':tags,'archive':archive}

def get_real_comment(comment):
    start = '<blockquote>'
    end = '>etouqkcolb/<'
    index = comment.find(start)
    if index == -1:
        return comment
    else:
        before = comment[:index]
    comment = ''.join(reversed(comment))
    index = comment.find(end)
    after = comment[:index]
    after = ''.join(reversed(after))
    comment = before + after
    return comment
        
