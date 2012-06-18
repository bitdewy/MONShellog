from django.conf.urls import patterns, include, url
from django.contrib import admin
from MONShellog.blog.feeds import *
from django.conf import settings
from django.conf.urls.static import static
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
    (r'^admin/(.*)', include(admin.site.urls)),
    (r'^$', 'MONShellog.blog.views.index'),
    (r'^archive/(?P<year>\d{4})/(?P<month>(\d{1,2})?)/$', 'MONShellog.blog.views.month'),
    (r'^archives/$', 'MONShellog.blog.views.archive'),
    (r'^links/$', 'MONShellog.blog.views.link'),
    (r'^entries/$', 'MONShellog.blog.views.entries'),
    (r'^comments/$', 'MONShellog.blog.views.comments'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',{'feed_dict': feeds}),
    url(r'^entry/(?P<key>.*)/$', 'MONShellog.blog.views.entry',name = 'entry'),
    url(r'^category/(?P<cat>.*)/$', 'MONShellog.blog.views.category',name = 'cate'),
    url(r'^tag/(?P<tag>.*)/$', 'MONShellog.blog.views.tag',name = 'tag'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
