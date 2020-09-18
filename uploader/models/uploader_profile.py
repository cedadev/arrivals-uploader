""" Module declaring the UploaderProfile model. """

__author__ = "William Tucker"
__date__ = "2017-08-10"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os

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

    @property
    def upload_path(self):

        prefix = os.path.commonprefix([settings.USERS_DIR, self.data_directory])
        if len(prefix) > 1:
            return os.path.relpath(self.data_directory, settings.USERS_DIR)
        else:
            return self.data_directory

    def __str__(self):
        return self.user.username
