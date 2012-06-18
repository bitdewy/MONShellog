from django.contrib import admin
from blog.models import Category, Comment, Entry, Link, Tag

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','detail')
    
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['author','body']
    list_display = ('entry','author','email','pub_date','IP','agent')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    
class EntryAdmin(admin.ModelAdmin):
    search_fields = ['headline','category']
    list_display = ('headline','category','pub_date','hits','comment_count','allow_comment','status')
    list_filter = ['category','pub_date','status']
    date_hierarchy = 'pub_date'
    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/js/admin.textarea.js',
              )
    
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name','site','detail')
    
class TagAdmin(admin.ModelAdmin):
    list_display =('name','count')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Link,LinkAdmin)
admin.site.register(Entry,EntryAdmin)
admin.site.register(Tag,TagAdmin)
