""" Module declaring the UploaderProfile model. """

__author__ = "William Tucker"
__date__ = "2017-08-10"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.conf import settings
from django.db import models


class UploaderProfile(models.Model):
    '''
    A user profile containing uploader-specific information
    '''
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_directory = models.TextField(blank=True)
    
    visible_ftp_password = models.TextField(blank=True)
    visible_rsync_password = models.TextField(blank=True)
    
    def __str__(self):
        return 'Uploader: {}'.format(self.user.username)
