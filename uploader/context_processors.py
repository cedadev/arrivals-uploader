""" Context processors for the app. """

__author__ = "William Tucker"
__date__ = "2017-10-18"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.contrib.sites.models import Site
from django.conf import settings


def site(request):
    
    return {'site': Site.objects.get_current()}
