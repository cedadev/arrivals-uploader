""" Functions for managing FTP accounts. """

__author__ = "William Tucker"
__date__ = "2018-08-02"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import pexpect
import logging

from django.conf import settings
from uploader.utils.password import generate_password
from uploader.exceptions import NoUploaderProfile, FtpCommandTimeout


logger = logging.getLogger(__name__)


def generate_visible_ftp_password(user):
    set_ftp_password(user, generate_password(), is_visible=True)


def set_ftp_password(user, password, is_visible=False):
    
    if not password or not isinstance(password, str):
        return ValueError('Password must not be empty')
    
    if not user.uploaderprofile:
        raise NoUploaderProfile('User missing uploaderprofile')
    
    username = user.username
    uid = settings.FTP_UID
    gid = settings.FTP_GID
    data_directory = user.uploaderprofile.data_directory
    
    ftp_files_directory, auth_user_file = os.path.split(settings.FTP_AUTH_USER_FILE)
    
    # Run ftpasswd command to create a new ftp user
    # or update the password of an existing user
    command = (f'ftpasswd --passwd --name={username} --uid={uid} --gid={gid} '
               f'--home={data_directory} --shell=/bin/false --file={auth_user_file}')
    
    # try:
        
    #     child = pexpect.spawn(command, cwd=ftp_files_directory, timeout=5)
        
    #     # Supply password
    #     child.expect('[Pp]assword:')
    #     child.sendline(password)
    #     child.expect('[Pp]assword:')
    #     child.sendline(password)
        
    #     child.expect(pexpect.EOF)
        
    # except pexpect.TIMEOUT:
        
    #     logger.error('Timeout running FTP command')
    #     raise FtpCommandTimeout('Command timeout')
    
    # # Make the password visible on the user's FTP account page
    # if is_visible:
    #     user.uploaderprofile.visible_ftp_password = password
    # else:
    #     user.uploaderprofile.visible_ftp_password = ''
    
    # user.uploaderprofile.save()
