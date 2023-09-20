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


good_path_regex = re.compile('^[\w\./-]*$')


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
        path = os.path.join(arrivals_dir, stream, rel_dir, new_dir)
        path = os.path.normpath(path)

        # check stream defined
        if not get_stream(request.user, stream):
            return render(request, "uploader/error.html", context={"error_message": "Need an upload route to make a directory"})

        # check for badness
        if not path.startswith(arrivals_dir):
            return render(request, "uploader/error.html", context={"error_message": "Could not make sense of directory name"})

        if not os.path.exists(path):
            os.mkdir(path)

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
        old_path = os.path.join(arrivals_dir, stream, rel_dir, old_filename)
        new_path = os.path.join(arrivals_dir, stream, rel_dir, new_filename)
        new_path = os.path.normpath(new_path)

        # check for badness
        assert new_path.startswith(arrivals_dir)

        os.rename(old_path, new_path)

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
        path = os.path.join(arrivals_dir, stream, rel_dir, filename)
        path = os.path.normpath(path)

        # check for badness
        assert path.startswith(arrivals_dir)

        if os.path.islink(path):
            os.unlink(path)
        elif not os.path.exists(path):
            pass
        elif os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path) and len(os.listdir(path)) == 0:
            os.rmdir(path)
        else:
            pass

        url_params = { 'stream': stream }
        url_params.update(kwargs) # combine url_params with the request kwargs
        if rel_dir:
            url_params['rel_dir'] = rel_dir
        return redirect("browse", **url_params)

    elif request.method == "GET":
        stream = request.GET["stream"]
        rel_dir = request.GET["dir"]
        filename = request.GET["filename"]
        return render(request, "uploader/delete_confirm.html", context={"stream": stream, "rel_dir": rel_dir,
                                                               "filename": filename})


@data_directory_required
def fix(request, fix_type, fix_info, fix_function,*args,**kwargs):
    """Apply a fix a direcory"""
    arrivals_dir = request.user.uploaderprofile.data_directory

    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        stream = request.GET["stream"]
        rel_dir = request.GET["dir"]
        path = os.path.join(arrivals_dir, stream, rel_dir)
        path = os.path.normpath(path)

    if "confirmed" not in request.GET:
        return render(request, 'uploader/confirm_fix.html',
                      {"fix_type": fix_type, 'fix_info': fix_info, "rel_dir": rel_dir, "stream":stream})
    else:
        fix_function(path)

    url_params = { 'stream': stream }
    url_params.update(kwargs)  # combine url_params with the request kwargs
    if rel_dir:
        url_params['rel_dir'] = rel_dir
    return redirect("browse", **url_params)


def fix_chars(request,*args,**kwargs):
    """Apply a fix to bad characters in file names"""

    # make fix function
    def fix_filenames(start_dir):
        for directory, dirs, files in os.walk(start_dir, topdown=False):
            for f in files + dirs:
                path = os.path.join(directory, f)
                if not good_path_regex.match(f):
                    new_name = unidecode.unidecode(f)
                    new_name = re.sub('%20', '_', new_name).strip()
                    new_name = re.sub('[+&]', '_and_', new_name).strip()
                    new_name = re.sub('[@]', '_at_', new_name).strip()
                    new_name = re.sub('[^\w\s\.-]', '', new_name).strip()
                    new_name = re.sub('\s+', '_', new_name)
                    print(new_name)

                    new_path = os.path.join(directory, new_name)
                    os.rename(path, new_path)

    return fix(request, "fix_chars", """Change filenames so that & and + become _and_, @ becomes _at_, spaces
                become underscores and other charaters are mapped to plain ASCII or removed.""", fix_filenames, **kwargs)


def fix_unzip(request,*args,**kwargs):
    """Apply a fix to unzip any .zip files"""

    # make fix function
    def _fix_unzip(start_dir):
        for directory, _, files in os.walk(start_dir):
            for f in files:
                _, ext = os.path.splitext(f)
                if ext == ".zip":
                    path = os.path.join(directory, f)
                    with ZipFile(path) as z:
                        z.extractall(directory)
                        os.unlink(path)

    return fix(request, "fix_unzip", """Expand compressed or aggregated files like .zip, .tar, .gz.""", _fix_unzip,**kwargs)


def fix_zero(request,*args,**kwargs):
    """Apply a fix to remove zero length files"""

    # make fix function
    def _fix_zero(start_dir):
        for directory, _, files in os.walk(start_dir):
            for f in files:
                path = os.path.join(directory, f)
                size = os.path.getsize(path)
                if size == 0:
                    os.unlink(path)
                    print("REMOVE zero length file %s " % path)

    return fix(request, "fix_zero_length", """Remove any files with no content.""", _fix_zero,**kwargs)


def fix_empty(request,*args,**kwargs):
    """Apply a fix to remove empty directories - including directories that contain only other empty directories.
    Does not remove the top level directory."""

    # make fix function
    def _fix_empty(start_dir):
        for directory, dirs, files in os.walk(start_dir, topdown=False):
            if directory == start_dir:
                pass
            if len(dirs) == 0 and len(files) == 0:
                print("Removing Empty directory")
                os.rmdir(directory)

    return fix(request, "fix_empty_dir", """Remove any empty directories.""", _fix_empty,**kwargs)


def fix_delete_dir(request,*args,**kwargs):
    """Apply a fix to remove empty directories"""

    # make fix function
    def _fix_delete_dir(start_dir):
        for f in os.listdir(start_dir):
            path = os.path.join(start_dir, f)
            if os.path.islink(path):
                os.unlink(path)
            elif os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    return fix(request, "fix_delete_dir", """Recursively delete this directory.""", _fix_delete_dir,**kwargs)


def fix_links(request,*args,**kwargs):
    """Apply a fix to remove symlinks"""

    def _fix_links(start_dir):
        for directory, dirs, files in os.walk(start_dir):
            for f in files + dirs:
                path = os.path.join(directory, f)
                if os.path.islink(path):
                    os.unlink(path)
                    print("REMOVE - %s " % path)

    return fix(request, "fix_remove_links", """Remove any symbolic links.""", _fix_links,**kwargs)
