""" Utility functions related to Streams. """

__author__ = "William Tucker"
__date__ = "2017-08-10"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import logging

from collections import namedtuple
from django.conf import settings
from uploader.models.uploader_profile import UploaderProfile
from uploader.models.stream import Stream
from uploader.exceptions import NoUploaderProfile,\
    NoDataDirectory, MissingDataDirectory
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


def create_data_directory(user):
    """Creates a new data directory for a user in the application's USERS_DIR"""
    
    uploader_profile, _ = UploaderProfile.objects.get_or_create(user=user)
    
    # Create the user's data upload directory
    path = os.path.join(settings.USERS_DIR, user.username)
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)
    
    uploader_profile.data_directory = path
    uploader_profile.save()


def get_data_directory(user):
    """Retrieve the data directory associated with a user"""
    
    data_directory = None
    if not user.is_anonymous:
        try:
            uploader_profile = UploaderProfile.objects.get(user=user)
            data_directory = uploader_profile.data_directory
            
        except ObjectDoesNotExist:
            raise NoUploaderProfile
    
    if not data_directory:
        raise NoDataDirectory
    elif not os.path.exists(data_directory):
        raise MissingDataDirectory
    else:
        return data_directory


def try_get_data_directory(user):
    
    try:
        return get_data_directory(user)
    except:
        return None


def get_stream(user, stream_name):
    """Retrieve a single user stream"""
    
    try:
        stream = Stream.objects.get(owner=user.uploaderprofile, name=stream_name)
    except ObjectDoesNotExist:
        stream = None

    if not stream:
        try:
            data_directory = get_data_directory(user)
        except (NoUploaderProfile, NoDataDirectory, MissingDataDirectory):
            return None
        
        stream_names = os.listdir(data_directory)
        if stream_name in stream_names:
            
            path = os.path.join(data_directory, stream_name)

            UnknownStream = namedtuple('UnknownStream', ['name', 'path'])
            stream = UnknownStream(name=stream_name, path=path)

    return stream


def get_streams(user, include_unknown=False):
    """Retrieve the upload streams associated with a user"""
    
    try:
        data_directory = get_data_directory(user)
        directory_names = os.listdir(data_directory)
        
    except NoUploaderProfile:
        return []
    except (NoDataDirectory, MissingDataDirectory):
        directory_names = []
    
    streams = []
    stream_names = []
    for stream in Stream.objects.filter(owner=user.uploaderprofile):
        streams.append(stream)
        stream_names.append(stream.name)
    
    if include_unknown:

        unknown_streams = []
        for name in directory_names:
            
            if name in stream_names:
                pass
            else:
                path = os.path.join(user.uploaderprofile.data_directory, name)

                UnknownStream = namedtuple('UnknownStream', ['name', 'path'])
                unknown_streams.append(UnknownStream(name=name, path=path))
    
        return streams, unknown_streams
    
    else:
        return streams

def update_stream(user, new_name, old_name, stored=True):
    if os.path.basename(new_name) != new_name:
        raise ValueError("'{}' is not a valid new stream name".format(new_name))
        return False

    data_directory = get_data_directory(user)
    new_path = os.path.join(data_directory, new_name)
    old_path = os.path.join(data_directory, old_name)
    
    if not os.path.abspath(new_path).startswith(data_directory):
        raise ValueError("Path '{}' not in user data directory".format(stream_path))
        return False

    if not os.path.exists(new_path):
        os.rename(old_path, new_path)

        stream = Stream.objects.get(name=old_name)
        stream.name = new_name
        stream.path = new_path
        
        stream.save()
        return stream
    else:
        return False

def create_stream(user, stream_name, stored=True):
    
    if os.path.basename(stream_name) != stream_name:
        raise ValueError("'{}' is not a valid stream name".format(stream_name))
    
    data_directory = get_data_directory(user)
    stream_path = os.path.join(data_directory, stream_name)
    
    if not os.path.abspath(stream_path).startswith(data_directory):
        raise ValueError("Path '{}' not in user data directory".format(stream_path))
    
    if not os.path.exists(stream_path):
        
        stream = None
        if stored:
            stream = Stream.objects.create(owner=user.uploaderprofile, path=stream_path)
            stream.save()
        else:
            os.mkdir(stream)
        
        return stream


def create_directory(user, stream_name, relative_path, directory_name):
    
    data_directory = get_data_directory(user)
    stream = os.path.join(data_directory, stream_name)
    new_directory_path = os.path.join(stream, relative_path, directory_name)
    
    if not os.path.abspath(new_directory_path).startswith(data_directory):
        raise ValueError("Path '{}' not in user data directory".format(new_directory_path))
    
    if not os.path.abspath(new_directory_path).startswith(stream):
        raise ValueError("Stream '{}' does not exist".format(stream_name))
    
    if not os.path.exists(os.path.basename(new_directory_path)):
        raise ValueError("Base path '{}' does not exist".format(
            os.path.basename(new_directory_path)))
    
    os.mkdir(new_directory_path)
