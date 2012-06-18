from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.feeds import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

feeds = {
         'rss': RecentEntriesRSS,
         'atom':RecentEntriesAtom
        }

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MONShellog.views.home', name='home'),
    # url(r'^MONShellog/', include('MONShellog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^admin/(.*)', admin.site.root),
    (r'^$', 'blog.views.index'),
    (r'^archive/(?P<year>\d{4})/(?P<month>(\d{1,2})?)/$', 'blog.views.month'),
    (r'^archives/$', 'blog.views.archive'),
    (r'^links/$', 'blog.views.link'),
    (r'^entries/$', 'blog.views.entries'),
    (r'^comments/$', 'blog.views.comments'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',{'feed_dict': feeds}),
    url(r'^entry/(?P<key>.*)/$', 'blog.views.entry',name = 'entry'),
    url(r'^category/(?P<cat>.*)/$', 'blog.views.category',name = 'cate'),
    url(r'^tag/(?P<tag>.*)/$', 'blog.views.tag',name = 'tag'),
)
