""" Rsync request handling. """

__author__ = "William Tucker"
__date__ = "2018-08-02"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import re
import json
import stat

from django.conf import settings
from json.decoder import JSONDecodeError
from uploader.exceptions import RsyncRequestReadError


class RsyncRequest(object):
    
    DEFAULT_FILENAME_TEMPLATE = '{username}_req.json'
    DEFAULT_FILENAME_REGEX = '(.*)(?=_req.json)'
    
    FAILED_DIRNAME = 'failed'
    FAILED_PREFIX = 'failed_'
    
    def __init__(self, file_path=None, username=None, password=None, data_directory=None):
        
        self.file_path = file_path
        if file_path and os.path.isfile(file_path):
            with open(file_path, 'r') as request_file:
                
                try:
                    self._data = json.load(request_file)
                except JSONDecodeError as e:
                    raise RsyncRequestReadError(f"Error decoding file at {file_path}", e, file_path)
        else:
            self._data = {
                'username': username,
                'uid': settings.RSYNC_UID,
                'password': password,
                'data_directory': data_directory,
            }
    
    @property
    def username(self):
        return self._data.get('username')
    
    @property
    def password(self):
        return self._data.get('password')
    
    @property
    def data_directory(self):
        return self._data.get('data_directory')
    
    def as_dictionary(self):
        return self._data
    
    def remove(self):
        
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
    
    def write(self, requests_directory):
        
        filename_template = getattr(settings,
            'RSYNC_REQUEST_FILENAME_TEMPLATE', RsyncRequest.DEFAULT_FILENAME_TEMPLATE)
        
        request_data = {
            'username': self.username,
            'uid': self._data['uid'],
            'password': self.password,
            'data_directory': self.data_directory,
        }
        
        request_filename = filename_template.format(username=self.username)
        file_path = os.path.join(requests_directory, request_filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        with open(file_path, 'w') as request_file:
            json.dump(request_data, request_file)
        
        # File contains sensitive information
        # Set to read only
        os.chmod(file_path, stat.S_IREAD | stat.S_IWRITE)
        
        self.file_path = file_path
    
    @classmethod
    def get_failed_file_path(cls, file_path, requests_directory):
        
        failed_directory = os.path.join(requests_directory, RsyncRequest.FAILED_DIRNAME)
        if not os.path.exists(failed_directory):
            os.mkdir(failed_directory)
        
        new_file_name = RsyncRequest.FAILED_PREFIX + os.path.basename(file_path)
        
        return os.path.join(failed_directory, new_file_name)
    
    @classmethod
    def read_requests(cls, requests_directory=None, filename_regex=None):
        """ Read all the rsync requests in a directory
        Returns a generator for RsyncRequest objects
        """
        
        if not requests_directory:
            requests_directory = settings.RSYNC_REQUESTS_DIR
        
        if not filename_regex:
            filename_regex = getattr(settings,
                'RSYNC_REQUEST_FILENAME_REGEX', RsyncRequest.DEFAULT_FILENAME_REGEX)
        
        for (root, _, file_names) in os.walk(requests_directory):
            for file_name in file_names:
                
                match = re.match(filename_regex, file_name)
                if match:
                    
                    request = RsyncRequest(os.path.join(root, file_name))
                    if request.username == match.group(1):
                        yield request
            
            break
