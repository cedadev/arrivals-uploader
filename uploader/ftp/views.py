""" Views related to rsync or FTP account access. """

__author__ = "William Tucker"
__date__ = "2018-03-13"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.shortcuts import render, redirect

from uploader.ftp.forms import FtpPasswordChangeForm
from uploader.ftp.utils import generate_visible_ftp_password, set_ftp_password


def ftp_random_password(request):
    
    generate_visible_ftp_password(request.user)
    return redirect('browse')


def ftp_access(request):
    
    if request.method=='POST':
        
        form = FtpPasswordChangeForm(request.POST)
        if form.is_valid():
            
            cleaned_data = form.cleaned_data
            password = cleaned_data.get('password')
            
            set_ftp_password(request.user, password)
            
            return redirect('browse')
    
    else:
        form = FtpPasswordChangeForm()
    
    return render(request, 'uploader/ftp/access.html', {'form': form})
