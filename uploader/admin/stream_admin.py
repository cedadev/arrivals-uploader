""" Admin module for the Stream model. """

__author__ = "William Tucker"
__date__ = "2018-04-24"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django import forms
from django.contrib import admin

from uploader.models.stream import Stream


class StreamChangeForm(forms.ModelForm):
    
    class Meta:
        model = Stream
        fields = ('owner', 'path', 'name',)


class StreamAdmin(admin.ModelAdmin):
    
    form = StreamChangeForm
    
    readonly_fields = ('owner', 'path',)


admin.site.register(Stream, StreamAdmin)
