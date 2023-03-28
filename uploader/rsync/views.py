""" Views related to rsync or FTP account access. """

__author__ = "William Tucker"
__date__ = "2018-03-13"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.shortcuts import render, redirect

from uploader.rsync.forms import RsyncPasswordChangeForm
from uploader.rsync.utils import generate_visible_rsync_password, set_rsync_password


def rsync_random_password(request,**kwargs):
    
    generate_visible_rsync_password(request.user)
    return redirect('browse',**kwargs)


def rsync_access(request,**kwargs):
    
    if request.method=='POST':
        
        form = RsyncPasswordChangeForm(request.POST)
        if form.is_valid():
            
            cleaned_data = form.cleaned_data
            password = cleaned_data.get('password')
            
            set_rsync_password(request.user, password)
            
            return redirect('browse',**kwargs)
    
    else:
        form = RsyncPasswordChangeForm()
    
    return render(request, 'uploader/rsync/access.html', {'form': form})

