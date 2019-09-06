""" Exceptions used by the app. """

__author__ = "William Tucker"
__date__ = "2017-08-14"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


class UploaderProfileException(Exception):
    """Exception related to a user's uploader profile"""
    pass

class NoUploaderProfile(UploaderProfileException):
    """The user object does not have an uploader profile"""
    pass

class NoDataDirectory(UploaderProfileException):
    """The uploader profile does not have an associated data directory"""
    pass

class MissingDataDirectory(UploaderProfileException):
    """The user's data directory is missing or inaccessible"""
    pass

class FtpCommandTimeout(Exception):
    """An FTP command timed out"""
    pass

class StreamPathNotFound(Exception):
    """Couldn't locate a stream directory"""
    pass

class RsyncRequestReadError(Exception):
    """Failed to read rsync request file"""
    
    def __init__(self, message, errors, file_path):
        super().__init__(message)
        
        self.errors = errors
        self.file_path = file_path

class RsyncUpdateException(Exception):
    """Exception thrown by an rsync update attempt"""
    pass
