from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from MONShellog.blog.models import Entry

class RecentEntriesRSS(Feed):
    title = _('Rencent Entries | Monshellog')
    link = '/feeds/rss/'
    description = _('Recent entries posted to Monshellog')
    
    def items(self):
        return Entry.objects.filter(status__exact='publish').order_by('-id')[:10]
    
    def item_pubdate(self, item):
        return item.pub_date

    author_email = 'shello1987@gmail.com,snowei1988@gmail.com'

class RecentEntriesAtom(RecentEntriesRSS):
    feed_type = Atom1Feed
    link = '/feeds/atom/'
    title_template = 'feeds/rss_title.html'
    description_template = 'feeds/rss_description.html'
    subtitle = RecentEntriesRSS.description

