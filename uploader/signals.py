""" Signals used by the app. """

__author__ = "William Tucker"
__date__ = "2018-03-14"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from uploader.utils.streams import create_data_directory


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_uploader_profile(sender, instance, created, **kwargs):
    '''
    Called when a Django user is saved
    '''
    
    # We are only interested in newly created users
    if created:
        if not hasattr(settings, 'AUTO_CREATE_DATA_DIR') or settings.AUTO_CREATE_DATA_DIR:
            create_data_directory(instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_uploader_profile(sender, instance, **kwargs):
    '''
    Called when a Django user is saved
    '''
    
    if hasattr(instance, 'uploaderprofile'):
        instance.uploaderprofile.save()
