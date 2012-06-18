from django.template import Library
from MONShellog.blog.models import Comment,Link
from MONShellog.blog.tools import *

register = Library()

@register.inclusion_tag('sidebar.html', takes_context = True)
def get_sidebar(context):
    data = get_archive()
    data['links'] = Link.objects.all()
    data['comments'] = Comment.objects.filter(entry__status = 'publish').order_by('-pub_date')[:10]
    for comment in data['comments']:
        comment.body = get_real_comment(comment.body)
    data['entries'] = data['entries'][:10]
    data['tags'] = data['tags'][:40]
    return data

