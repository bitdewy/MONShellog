from django import forms
from django.utils.translation import ugettext as _

input_attrs = {'class':'comments-input',
               'size':'35',
               'tabindex':'1'
               }
textarea_attrs = { 'class': 'form-textarea',
                   'cols':'100',
                   'rows':'5',
                   'tabindex':'4'
                  }

class CommentForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput(attrs = input_attrs),
                           max_length=16,
                           )
    
    email = forms.EmailField(widget=forms.TextInput(attrs = input_attrs))
    
    url = forms.URLField(widget=forms.TextInput(attrs = input_attrs),
                         required=False, label = _('site/blog'))
    
    comment = forms.CharField(widget=forms.Textarea(attrs=textarea_attrs),
                              max_length=1536,
                              )
