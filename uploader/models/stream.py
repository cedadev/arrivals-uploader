""" Module declaring the Stream model. """

__author__ = "William Tucker"
__date__ = "2018-04-24"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import yaml

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from uploader.models.uploader_profile import UploaderProfile


class Stream(models.Model):
    '''
    Class representing a data stream
    '''
    
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z-_]*$',
        'Only alphanumeric characters and hyphens/underscores are allowed.'
    )
    
    owner = models.ForeignKey(UploaderProfile, on_delete=models.CASCADE)
    
    path = models.CharField(max_length=100)
    name = models.CharField(max_length=30, validators=[alphanumeric])
    
    def clean(self):
        
        if self.path and os.path.exists(self.path):
            raise ValidationError(('Stream already exists.'))
    
    def save(self, *args, **kwargs):
        
        if not self.path:
            
            directory = self.owner.data_directory
            self.path = os.path.join(directory, self.name)
            
        elif not self.name:
            self.name = os.path.basename(self.path)
        
        # Create the directory if it does not exist
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        super(Stream, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)
