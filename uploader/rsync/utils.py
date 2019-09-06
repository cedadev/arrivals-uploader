""" Utilities for rsync accounts. """

__author__ = "William Tucker"
__date__ = "2018-08-02"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.conf import settings
from uploader.utils.password import generate_password
from uploader.exceptions import NoUploaderProfile

from uploader.rsync.update.request import RsyncRequest


def generate_visible_rsync_password(user):
    set_rsync_password(user, generate_password(), is_visible=True)


def set_rsync_password(user, password, is_visible=False):
    
    if not password or not isinstance(password, str):
        return ValueError('Password must not be empty')
    
    if not user.uploaderprofile:
        raise NoUploaderProfile('User missing uploaderprofile')
    
    username = user.username
    rsync_request = RsyncRequest(
        username=username, password=password, data_directory=user.uploaderprofile.data_directory)
    rsync_request.write(settings.RSYNC_REQUESTS_DIR)
    
    # Make the password visible on the user's Rsync account page
    if is_visible:
        user.uploaderprofile.visible_rsync_password = password
    else:
        user.uploaderprofile.visible_rsync_password = ''
    
    user.uploaderprofile.save()
