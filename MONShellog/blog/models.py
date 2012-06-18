from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
# Create your models here.

ENTRY_STATUS = (
               ('publish',_('Publish')),
               ('draft',_('Draft')),
              )
ALLOW_COMMENT = (
                 ('yes',_('Yes')),
                 ('no',_('No')),
                )

class Category(models.Model):
    name = models.CharField(_('Category'),unique=True,max_length=16,help_text=_('The name of this category'))
    slug = models.SlugField(_('Slug'),unique=True,max_length=16,help_text=_('Use as URL'))
    detail = models.CharField(_('Description'),blank=True,max_length=255,help_text=_('description this category,you can leave it blank'))
    
    class Meta:
        verbose_name_plural = _('Categories')
        verbose_name = _('Category')

    def get_absolute_url(self):
        return reverse('cate', args=[self.slug])

    def __unicode__(self):
        return self.name    
    
class Tag(models.Model):
    name = models.CharField(_('Tag name'),unique=True,max_length=16)
    slug = models.SlugField(_('Slug'),unique=True,max_length=16,help_text=_('Use as URL'))
    count = models.IntegerField(_('Reference count'),default=0,editable=False)
    
    class Meta:
        verbose_name_plural = _('Tags')
        verbose_name = _('Tag')

    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])
    
    def __unicode__(self):
        return self.name

class Entry(models.Model):
    category = models.ForeignKey(Category,verbose_name =  _('Category'),null=True,blank=True)
    headline = models.CharField(_('title'),max_length=255)
    body = models.TextField(_('Content'))
    pub_date = models.DateTimeField(_('Published Date'),auto_now_add=True)
    hits = models.IntegerField(_('Hits'),default=0,editable=False)
    tags = models.ManyToManyField(Tag,verbose_name=_('Tags'),null=True,blank=True)
    status = models.CharField(_('status'),max_length = 8,choices=ENTRY_STATUS)
    allow_comment = models.CharField(_('Allow comment or not'),max_length = 8,choices=ALLOW_COMMENT)
    comment_count = models.IntegerField(_('Comment count'),default=0,editable=False)
    
    class Meta:
        verbose_name_plural = _('entries')
        verbose_name = _('entry')
    
    def save(self,force_insert=False, force_update=False):         
        super(Entry,self).save(force_insert, force_update)
        if self.tags:
            all_tags =  self.tags.all()
            for tag in all_tags:
                tag.count = tag.entry_set.count()
                tag.save()

    def get_absolute_url(self):
        return reverse('entry', args=[str(self.id)])
  
            
    def __unicode__(self):
        return self.headline    
    
class Comment(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_('Commented entry'),editable=False)
    author = models.CharField(_('Comment author'),max_length=16)
    IP = models.IPAddressField(verbose_name=_('IP address'),null=True,editable=False)
    agent = models.CharField(_('User agent information'),editable=False,max_length=255,null=True)
    email = models.EmailField(_('E-Mail'))
    site = models.URLField(_('Site'),null=True,blank=True,verify_exists=False)
    body = models.TextField(_('Comment content'))
    pub_date = models.DateTimeField(_('Published date'),auto_now_add=True,editable=False)

    class Meta:
        verbose_name_plural = _('Comments')
        verbose_name = _('Comment')

    def save(self,force_insert=False, force_update=False):                     
        super(Comment,self).save(force_insert, force_update)
        if self.entry:          
            self.entry.comment_count = self.entry.comment_set.count()
            self.entry.save()

    def __unicode__(self):
        return self.author
    
class Link(models.Model):
    name = models.CharField(_('Link name'),max_length=32)
    site = models.URLField(_('Site'),verify_exists=False)
    detail = models.CharField(_('Description'),null=True,blank=True,max_length=128)
    image_address = models.URLField(_('Image address'),null=True,blank=True,verify_exists=False)

    class Meta:
        verbose_name_plural = _('Links')
        verbose_name = _('Link')

    def __unicode__(self):
        return self.name
    
