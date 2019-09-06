""" Admin module for the UploaderProfile model. """

__author__ = "William Tucker"
__date__ = "2017-08-10"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django import forms
from django.contrib import admin

from uploader.models.uploader_profile import UploaderProfile


class UploaderProfileChangeForm(forms.ModelForm):
    
    class Meta:
        model = UploaderProfile
        fields = ('data_directory',)


class UploaderProfileAdmin(admin.ModelAdmin):
    
    form = UploaderProfileChangeForm
    
    readonly_fields = ('data_directory',)


admin.site.register(UploaderProfile, UploaderProfileAdmin)
