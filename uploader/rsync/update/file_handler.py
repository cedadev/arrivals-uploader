""" Rsync configuration file handling. """

__author__ = "William Tucker"
__date__ = "2018-07-25"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import re
import shutil

from datetime import datetime


class RsyncFileHandler():
    """ Class representing an rsync configuration file """
    
    def __init__(self, file_path, user_match_template, new_user_template):
        
        self.file_path = file_path
        
        self._user_match_template = user_match_template
        self._new_user_template = new_user_template
    
    def __enter__(self):
        
        self.open_file = open(self.file_path, 'r+')
        return self
    
    def __exit__(self, *args):
        self.open_file.close()
    
    def has_user_entry(self, user_data):
        
        # Reset file pointer
        self.open_file.seek(0)
        
        match_pattern = self._user_match_template.format(**user_data)
        for line in self.open_file.readlines():
            if re.match(match_pattern, line):
                return True
    
    def add_user_entry(self, user_data):
        
        # Read to the end
        self.open_file.read()
        
        new_entry = self._new_user_template.format(**user_data)
        self.open_file.write(f'\n{new_entry}')


class RsyncConf(RsyncFileHandler):
    
    USER_MATCH_TEMPLATE = '^\[{username}\].*'
    NEW_USER_TEMPLATE = ('[{username}]\n'
                         '  uid = {uid}\n'
                         '  path = {data_directory}\n'
                         '  auth users = {username}\n')
    
    def __init__(self, conf_file_path):
        super(RsyncConf, self).__init__(
                conf_file_path,
                self.USER_MATCH_TEMPLATE,
                self.NEW_USER_TEMPLATE
        )


class RsyncSecrets(RsyncFileHandler):
    
    USER_MATCH_TEMPLATE = '^{username}:.*'
    NEW_USER_TEMPLATE = '{username}:{password}'
    
    def __init__(self, secrets_file_path):
        super(RsyncSecrets, self).__init__(
                secrets_file_path,
                self.USER_MATCH_TEMPLATE,
                self.NEW_USER_TEMPLATE
        )
    
    def replace_password(self, user_data):
        
        # Create a backup file to prevent data loss
        directory, filename = os.path.split(self.file_path)
        backup_file = os.path.join(directory, f'{filename}.{datetime.now()}')
        shutil.copyfile(self.file_path, backup_file)
        
        # Reset file pointer
        self.open_file.seek(0)
        
        lines = self.open_file.readlines()
        # Remove file contents
        self.open_file.seek(0)
        self.open_file.truncate()
        
        match_pattern = self._user_match_template.format(**user_data)
        new_entry = self._new_user_template.format(**user_data)
        
        # Write lines back with modified credentials
        updated = False
        for line in lines:
            if not updated and re.match(match_pattern, line):
                
                self.open_file.write(f'{new_entry}\n')
                updated = True
                
            else:
                self.open_file.write(line)
        
        # Remove backup
        os.remove(backup_file)
        
        return updated
