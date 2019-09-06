""" Utility functions related to passwords. """

__author__ = "William Tucker"
__date__ = "2017-08-10"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import random
import string

from django.conf import settings


RANDOM_PASSWORD_LENGTH = 16


def generate_password(length = RANDOM_PASSWORD_LENGTH):
    
    if hasattr(settings, 'RANDOM_PASSWORD_LENGTH'):
        length = int(settings.RANDOM_PASSWORD_LENGTH)
    
    return ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))
