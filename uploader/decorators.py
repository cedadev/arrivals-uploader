""" App-specific decorators. """

__author__ = "William Tucker"
__date__ = "2018-03-13"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os

from functools import wraps
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import resolve_url, redirect
from uploader.models.uploader_profile import UploaderProfile
from uploader.exceptions import NoDataDirectory


def data_directory_required(function):
    
    @wraps(function)
    def inner(request, *args, **kwargs):
        
        try:
            uploader_profile = UploaderProfile.objects.get(user=request.user)
            if uploader_profile.data_directory and os.path.exists(uploader_profile.data_directory):
                return function(request, *args, **kwargs)
            else:
                raise NoDataDirectory
            
        except (ObjectDoesNotExist, NoDataDirectory):
            
            if hasattr(settings, 'MISSING_DATA_DIR_REDIRECT'):
                redirect_url = resolve_url(settings.MISSING_DATA_DIR_REDIRECT)
                return redirect(redirect_url)
            else:
                raise PermissionDenied
    
    return inner
