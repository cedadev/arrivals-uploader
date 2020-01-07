""" Tags related to uploader views. """

__author__ = "William Tucker"
__date__ = "2018-03-16"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os

from django import template

register = template.Library()


@register.filter
def list_directory(browse_dir, stream):

    directories = []
    files = []
    filenames = os.listdir(browse_dir)

    for filename in filenames:
        path = os.path.join(browse_dir, filename)
        exists = os.path.exists(path)
        is_dir = os.path.isdir(path)
        is_file = not is_dir

        link_to = None
        size = None
        if os.path.islink(path):
            link_to = os.readlink(path)
        elif exists:
            size = os.path.getsize(path)

        outside_stream = not os.path.realpath(path).startswith(stream.path)

        item = {
            'name': filename,
            'size': size,
            'is_dir': is_dir,
            'is_file': is_file,
            'link_to': link_to,
            'outside_stream': outside_stream,
            'exists': exists,
        }

        if is_dir:
            directories.append(item)
        else:
            files.append(item)

    return directories + files
