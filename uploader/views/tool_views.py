""" View for managing streams. """

__author__ = "William Tucker"
__date__ = "2018-03-13"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import re
import unidecode
import shutil

from zipfile import ZipFile

from django.shortcuts import render, redirect
from uploader.utils.streams import get_stream
from uploader.decorators import data_directory_required
import uploader.utils.tools as tools




@data_directory_required
def mkdir(request,*args,**kwargs):
    """Make a directory"""
    arrivals_dir = request.user.uploaderprofile.data_directory

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        stream = request.POST["stream"]
        rel_dir = request.POST["dir"]
        new_dir = request.POST["new_dir"]

        # check stream defined
        if not get_stream(request.user, stream):
            return render(request, "uploader/error.html", context={"error_message": "Need an upload route to make a directory"})

        if not tools.mkdir(os.path.join(arrivals_dir, stream), rel_dir, new_dir):
            return render(request, "uploader/error.html", context={"error_message": "Could not make new dir"})

        url_params = { 'stream': stream }
        url_params.update(kwargs)  # combine url_params with the request kwargs
        if rel_dir:
            url_params['rel_dir'] = rel_dir
        return redirect("browse", **url_params)

    elif request.method == "GET":
        stream = request.GET.get("stream")
        rel_dir = request.GET.get("dir")
        if stream:
            return render(request, "uploader/mkdir.html", context={"stream": stream, "rel_dir": rel_dir})
        else:
            return redirect('browse')


@data_directory_required
def rename(request,*args,**kwargs):
    """rename a file or directory"""
    arrivals_dir = request.user.uploaderprofile.data_directory

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        stream = request.POST["stream"]
        rel_dir = request.POST["dir"]
        old_filename = request.POST["filename"]
        new_filename = request.POST["new_name"]

        if not tools.rename(os.path.join(arrivals_dir, stream), rel_dir, old_filename, new_filename):
            raise Exception("Could not rename file")

        url_params = { 'stream': stream }
        url_params.update(kwargs)  # combine url_params with the request kwargs
        if rel_dir:
            url_params['rel_dir'] = rel_dir
        return redirect("browse", **url_params)

    elif request.method == "GET":
        stream = request.GET["stream"]
        rel_dir = request.GET["dir"]
        filename = request.GET["filename"]
        return render(request, "uploader/rename.html", context={"stream": stream, "rel_dir": rel_dir, "filename": filename})


@data_directory_required
def delete_file(request,*args,**kwargs):
    """Delete a file or empty directory"""
    arrivals_dir = request.user.uploaderprofile.data_directory

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        stream = request.POST["stream"]
        rel_dir = request.POST["dir"]
        filename = request.POST["filename"]

        stream_dir = os.path.join(arrivals_dir, stream)

        if not tools.delete_file(stream_dir, rel_dir, filename):
            raise Exception("Could not delete file")

        url_params = { 'stream': stream }
        url_params.update(kwargs) # combine url_params with the request kwargs
        if rel_dir:
            url_params['rel_dir'] = rel_dir
        return redirect("browse", **url_params)

    elif request.method == "GET":
        stream = request.GET["stream"]
        rel_dir = request.GET["dir"]
        filename = request.GET["filename"]
        return render(request, "uploader/delete_confirm.html", 
                      context={"stream": stream, "rel_dir": rel_dir, "filename": filename}
                      )


@data_directory_required
def fix(request, fix_type, fix_info, fix_function, *args, **kwargs):
    """Apply a fix a direcory"""
    arrivals_dir = request.user.uploaderprofile.data_directory

    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        stream = request.GET["stream"]
        rel_dir = request.GET["dir"]
        path = tools.join_norm_and_check_path(arrivals_dir, stream, rel_dir)
        if not path:  # Fail
            return redirect("browse", **url_params)
    if "confirmed" not in request.GET:
        return render(request, 'uploader/confirm_fix.html',
                      {"fix_type": fix_type, 'fix_info': fix_info, "rel_dir": rel_dir, "stream":stream})

    fix_function(path)

    url_params = { 'stream': stream }
    url_params.update(kwargs)  # combine url_params with the request kwargs
    if rel_dir:
        url_params['rel_dir'] = rel_dir
    return redirect("browse", **url_params)


def fix_chars(request,*args,**kwargs):
    """Apply a fix to bad characters in file names"""
    return fix(request, "fix_chars", """Change filenames so that & and + become _and_, @ becomes _at_, spaces
                become underscores and other characters are mapped to plain ASCII or removed.""", 
                tools.fix_filenames, **kwargs)


def fix_unzip(request,*args,**kwargs):
    """Apply a fix to unzip any .zip files"""
    return fix(request, "fix_unzip", """Expand compressed or aggregated files like .zip, .tar, .gz.""", 
               tools.fix_unzip,**kwargs)


def fix_zero(request,*args,**kwargs):
    """Apply a fix to remove zero length files"""

    return fix(request, "fix_zero_length", """Remove any files with no content.""", 
               tools.fix_zero,**kwargs)


def fix_empty(request,*args,**kwargs):
    """Apply a fix to remove empty directories - including directories that contain only other empty directories.
    Does not remove the top level directory."""

    return fix(request, "fix_empty_dir", """Remove any empty directories.""", 
               tools.fix_empty,**kwargs)


def fix_delete_dir(request,*args,**kwargs):
    """Apply a fix to remove empty directories"""

    return fix(request, "fix_delete_dir", """Recursively delete this directory.""", 
               tools.fix_delete_dir,**kwargs)


def fix_links(request,*args,**kwargs):
    """Apply a fix to remove symlinks"""
    return fix(request, "fix_remove_links", """Remove any symbolic links.""", 
               tools.fix_links,**kwargs)
