#!/usr/bin/env python

""" Script for automatically managing rsync accounts. """

__author__ = "William Tucker"
__date__ = "2017-09-05"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import argparse

from datetime import datetime

from uploader.exceptions import RsyncRequestReadError, RsyncUpdateException
from .file_handler import RsyncSecrets, RsyncConf
from .request import RsyncRequest


def process_request(request, conf_path, secrets_path):
    """ Updates an rsync conf and secrets file using
    information provided by an RsyncRequest object
    """
    
    try:
        with RsyncConf(conf_path) as conf, RsyncSecrets(secrets_path) as secrets:
            
            user_data = request.as_dictionary()
            
            if not conf.has_user_entry(user_data):
                conf.add_user_entry(user_data)
            
            if not secrets.has_user_entry(user_data):
                secrets.add_user_entry(user_data)
            else:
                secrets.replace_password(user_data)
        
    except Exception as e:
        raise RsyncUpdateException(e)
    
    request.remove()


def main():
    """ Runnable module which reads user rsync account change requests from
    json files and updates an rsync conf and secrets file in response
    """
    
    parser = argparse.ArgumentParser(description='Loads data from an XLSX file.')
    
    parser.add_argument('conf', type=str,
                        help='Path to the rsync config file')
    parser.add_argument('secrets', type=str,
                        help='Path to the rsync secrets file')
    parser.add_argument('requests_directory', type=str,
                        help='Location of rsync request json files')
    
    args = parser.parse_args()
    
    conf_path = args.conf
    if not conf_path:
        conf_path = input("Config file location:")
    
    secrets_path = args.secrets
    if not secrets_path:
        secrets_path = input("Secrets file location:")
    
    requests_directory = args.requests_directory
    if not requests_directory:
        requests_directory = input("Location of rsync requests:")
    
    # Parse request json files from directory
    request_results = []
    try:
        filename_regex = RsyncRequest.DEFAULT_FILENAME_REGEX
        for request in RsyncRequest.read_requests(requests_directory, filename_regex):
            
            try:
                
                process_request(request, conf_path, secrets_path)
                result = f"{os.path.basename(request.file_path)} [OK]"
                
            except RsyncUpdateException as e:
                
                failed_file_path = RsyncRequest.get_failed_file_path(
                    request.file_path, requests_directory)
                os.rename(request.file_path, failed_file_path)
                result = f"{os.path.basename(request.file_path)} [ERROR (moved to {failed_file_path})] - {e}"
            
            request_results.append(result)
        
    except RsyncRequestReadError as e:
        
        failed_file_path = RsyncRequest.get_failed_file_path(e.file_path, requests_directory)
        os.rename(e.file_path, failed_file_path)
        request_results.append((f"{os.path.basename(e.file_path)} "
                                f"[ERROR (moved to {failed_file_path})] - {e.errors}"))
    
    if len(request_results):
        
        results_string = "\n  ".join(request_results)
        print(f"[{datetime.now()}] Processed rsync requests:\n  {results_string}\n")
