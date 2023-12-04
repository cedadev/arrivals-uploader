import os
import re
import unidecode
import shutil
from multiprocessing import Process
import logging
from multiprocessing import Process
import logging

from zipfile import ZipFile


logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


def join_norm_and_check_path(base, relative, file) -> str:
    full_path = os.path.join(base, relative, file)
    full_path = os.path.normpath(full_path)
    if not full_path.startswith(base):
        return ""
    return full_path


def mkdir(stream_dir, relative_dir, new_dir) -> bool:
    full_path = join_norm_and_check_path(stream_dir, relative_dir, new_dir)
    
    if not full_path:
        return False

    if os.path.exists(full_path):
        return False
    
    os.mkdir(full_path)
    return True


def rename(stream_dir, relative_dir, old_file, new_file) -> bool:
    full_path = join_norm_and_check_path(stream_dir, relative_dir, old_file)
    new_full_path = join_norm_and_check_path(stream_dir, relative_dir, new_file)

    if not full_path or not new_full_path:
        return False
    if not os.path.exists(full_path):
        return False
    if full_path == new_full_path:
        return True
    if os.path.exists(new_full_path):
        return False
    
    os.rename(full_path, new_full_path)
    return True


def delete_file(stream_dir, relative_dir, file):
    full_path = join_norm_and_check_path(stream_dir, relative_dir, file)

    if not full_path:
        return False
    
    if not os.path.exists(full_path):
        return False
    
    def is_empty_dir(path):
        return os.path.isdir(path) and len(os.listdir(path)) == 0
    
    def is_non_empty_dir(path):
        return os.path.isdir(path) and len(os.listdir(path)) != 0
    
    if os.path.islink(full_path):
        os.unlink(full_path)
    elif os.path.isfile(full_path):
        os.unlink(full_path)
    elif is_empty_dir(full_path):
        os.rmdir(full_path)
    elif is_non_empty_dir(full_path):
        root, dir = os.path.split(full_path)
        new_name = root + "/.deleting-folder-{dir}"
        if not rename(root, "", dir, ".deleting-folder-{dir}"):
            return False
        p = Process(target=_delete_directory_recursive, args=(new_name, True))
        p.start()
        p.join(2)

    return True


def fix_filenames(start_dir):
    good_path_regex = re.compile('^[\w\./-]*$')
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


def fix_unzip(start_dir):
    for directory, _, files in os.walk(start_dir):
        for f in files:
            _, ext = os.path.splitext(f)
            if ext == ".zip":
                path = os.path.join(directory, f)
                with ZipFile(path) as z:
                    z.extractall(directory)
                    os.unlink(path)


def fix_zero(start_dir):
    for directory, _, files in os.walk(start_dir):
        for f in files:
            path = os.path.join(directory, f)
            size = os.path.getsize(path)
            if size == 0:
                os.unlink(path)
                print("REMOVE zero length file %s " % path)


def fix_empty(start_dir):
    for directory, _, files in os.walk(start_dir, topdown=False):
        if directory == start_dir:  # Do not remove the top level directory
            continue
        if len(os.listdir(directory)) == 0 and len(files) == 0:
            print(f"Removing Empty directory {directory}")
            os.rmdir(directory)


def _delete_directory_recursive(start_dir, delete_root=False):
    try:
        for f in os.listdir(start_dir):
            path = os.path.join(start_dir, f)
            if os.path.islink(path):
                os.unlink(path)
            elif os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        if delete_root:
            os.rmdir(start_dir)
    except OSError as e:
        logger.error(f"Error while Deleting files in folder `{start_dir}` - {e}")
        raise e


def fix_delete_dir(start_dir):
    # Deleting can take a long time when there are many large files
    p = Process(target=_delete_directory_recursive, args=(start_dir, False))
    p.start()
    p.join(2)  # wait for the delete thread to reduce issues, unless it takes a very long time


def fix_links(start_dir):
    for directory, dirs, files in os.walk(start_dir):
        for f in files + dirs:
            path = os.path.join(directory, f)
            if os.path.islink(path):
                os.unlink(path)
                print("REMOVE - %s " % path)
                