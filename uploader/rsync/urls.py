""" Rsync app URLs. """

__author__ = "William Tucker"
__date__ = "2019-09-06"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.urls import path

from uploader.rsync.views import rsync_random_password, rsync_access


urlpatterns = [
    path('generate/', rsync_random_password, name="rsync_random_password"),
    path('access/', rsync_access, name="rsync_access"),
]
