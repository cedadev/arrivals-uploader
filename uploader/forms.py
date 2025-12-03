""" Forms for app views. """

__author__ = "William Tucker"
__date__ = "2017-10-20"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django import forms
from django.conf import settings
from django.forms import Form, ValidationError
from django.template.defaultfilters import filesizeformat


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadForm(Form):
    
    # Default 2GB upload size
    MAX_FILE_SIZE = getattr(settings, 'MAX_UPLOAD_SIZE', 1024*1024*1024*2)
    
    files = MultipleFileField(label='Select files', required=False)

    class Meta:
        fields = ["files", ]

    def __init__(self, stream=None, rel_dir=None, *args, **kwargs):
        
        self.request = kwargs.pop("request")
        super(UploadForm, self).__init__(*args, **kwargs)
        
        self.stream = stream
        self.rel_dir = rel_dir
    
    def clean_files(self):

        files = self.request.FILES.getlist('files')

        for uploaded_file in files:
            if uploaded_file.size > self.MAX_FILE_SIZE:
                raise ValidationError((
                    f'{uploaded_file.name} is too big. Please keep file sizes '
                    f'under the limit of {filesizeformat(self.MAX_FILE_SIZE)}.'
                ))

        return files
