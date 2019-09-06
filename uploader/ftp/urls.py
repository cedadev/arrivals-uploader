""" FTP app URLs. """

__author__ = "William Tucker"
__date__ = "2019-09-06"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.urls import path

from uploader.ftp.views import ftp_random_password, ftp_access


urlpatterns = [
    path('generate/', ftp_random_password, name="ftp_random_password"),
    path('access/', ftp_access, name="ftp_access"),
]
