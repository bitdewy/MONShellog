from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator
from django.http import Http404,HttpResponseRedirect
from django.utils.dateformat import format
from datetime import datetime
from blog.models import Entry, Link, Comment
from blog.form import CommentForm
from blog.tools import *
PAGE_SIZE = 7

@render_to('index.html')
def index(request):
    entries_all = Paginator(Entry.objects.filter(status__exact = 'publish').order_by('-pub_date'),PAGE_SIZE)
    page_id = get_page_id(request.GET.get('page','1'))
    current_page = page(entries_all,page_id)   
    data = {
            'entries':current_page.object_list,
            'has_next':current_page.has_next(),
            'next':page_id + 1,
            'has_previous':current_page.has_previous(),
            'previous':page_id - 1 
           }
    return data

@render_to('entry.html')
def entry(request,key):
    try:
        current = get_object_or_404(Entry, pk = key)
        previous = Entry.objects.filter(id__lt = key).order_by('-id')[0]
    except(ValueError):
        raise Http404()        
    except(IndexError):
        previous = []
    try:
        next = Entry.objects.filter(id__gt = key).order_by('id')[0]
    except(IndexError):
        next = []
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(entry = current,
                               author=form.cleaned_data['author'],
                               email=form.cleaned_data['email'],
                               site=form.cleaned_data['url'],
                               IP=request.META['REMOTE_ADDR'],
                               body = form.cleaned_data['comment'],
                               agent=request.META['HTTP_USER_AGENT'],
                               pub_date = datetime.now())
            comment.save() 
            form = CommentForm()
            return HttpResponseRedirect(current.get_absolute_url() + '#respond')
    elif current.allow_comment == 'yes':
        form = CommentForm()
    else:
        form = None
    comments = list(Comment.objects.filter(entry__id = key).order_by('id'))
    comments = set_all_image(comments,36)
    if not request.session.get('current_hits_%s' % current.id):
        current.hits = current.hits + 1
        current.save()
        request.session['current_hits_%s' % current.id] = True;
    data = {'current':current,
            'comments':comments,
            'previous':previous,
            'next':next,
            'form':form }
    return data

@render_to('bar.html')
def category(request,cat):
    if cat == 'uncategories':
        entries = Entry.objects.filter(status__exact='publish',category__isnull = True)
    else:
        entries = Entry.objects.filter(status__exact='publish',category__slug = cat)
    try:
        category = entries[0].category
    except(IndexError):
        raise Http404()
    entries = Paginator(entries.order_by('-pub_date'),PAGE_SIZE)
    page_id = get_page_id(request.GET.get('page','1'))
    current_page = page(entries,page_id)
    data = {
            'name': 'Category',
            'category': category,
            'entries': current_page.object_list,
            'has_next': current_page.has_next(),
            'next': page_id + 1,
            'has_previous': current_page.has_previous(),
            'previous': page_id - 1 }
    return data

@render_to('bar.html')
def tag(request,tag):
    entries = Entry.objects.filter(status__exact='publish',tags__slug = tag)
    try:
        tag = entries[0].tags.get(slug = tag)
    except(IndexError):
        raise Http404()
    entries = Paginator(entries.order_by('-pub_date'),PAGE_SIZE)
    page_id = get_page_id(request.GET.get('page','1'))
    current_page = page(entries,page_id)
    data = {
            'name': 'Tag',
            'tag': tag,
            'entries': current_page.object_list,
            'has_next': current_page.has_next(),
            'next': page_id + 1,
            'has_previous': current_page.has_previous(),
            'previous': page_id - 1 }
    return data

@render_to('bar.html')
def month(request,year,month):
    try:
        year = int(year)
        month = int(month)
    except(ValueError):
        raise Http404()
    try:
        archive = format(datetime(year,month,1),'b,Y')
    except(ValueError):
        raise Http404()
    entries = Entry.objects.filter(pub_date__year = year,pub_date__month = month,status__exact = 'publish')
    if not entries:
        Http404()
    entries = Paginator(entries.order_by('-pub_date'),PAGE_SIZE)
    page_id = get_page_id(request.GET.get('page','1'))  
    current_page = page(entries,page_id)    
    data = {
            'name': 'Archive',
            'archive': archive,
            'entries': current_page.object_list,
            'has_next': current_page.has_next(),
            'next': page_id + 1,
            'has_previous': current_page.has_previous(),
            'previous': page_id - 1 }
    return data


@render_to('archive.html')
def archive(request):
    data = get_archive()
    del data['entries']
    for tag in data['tags']:
        if tag.weight == 0:
            tag.style = 'font-size:12px; color:#6994b9;'
        if tag.weight == 1:
            tag.style = 'font-size:13.78px; color:#527ca6;'
        if tag.weight == 2:
            tag.style = 'font-size:15.56px; color:#3c6493;'
        if tag.weight == 3:
            tag.style = 'font-size:17.33px; color:#254d80;'
        if tag.weight == 4:
            tag.style = 'font-size:19.11px; color:#0f356d;'        
    return data

@render_to('link.html')
def link(request):
    links = Link.objects.all()
    return {'links':links}

@render_to('entries.html')
def entries(request):
    entries = Paginator(Entry.objects.filter(status__exact = 'publish').order_by('-pub_date'),40)       
    page_id = get_page_id(request.GET.get('page','1'))
    current_page = page(entries,page_id)
    data = {
            'entries': current_page.object_list,
            'has_next': current_page.has_next(),
            'next': page_id + 1,
            'has_previous': current_page.has_previous(),
            'previous': page_id - 1 }
    return data

@render_to('comments.html')
def comments(request):
    comments = list(Comment.objects.all().order_by('-id')[:30])
    comments = set_all_image(comments,40)
    for comment in comments:
        comment.body = get_real_comment(comment.body)
    return {'comments':comments}

