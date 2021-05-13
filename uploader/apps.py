""" Apps module. """

__author__ = "William Tucker"
__date__ = "2017-07-28"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.apps import AppConfig


class ArrivalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploader'
