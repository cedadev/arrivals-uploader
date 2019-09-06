""" Views related to the Stream model. """

__author__ = "William Tucker"
__date__ = "2018-04-25"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from uploader.decorators import data_directory_required
from uploader.models.stream import Stream
from django.urls.base import reverse


@method_decorator(data_directory_required, name='dispatch')
class CreateStreamView(CreateView):
    '''
    Form view handling stream creation
    '''
    
    model = Stream
    fields = ['name']
    
    def form_valid(self, form):
        
        form.instance.owner = self.request.user.uploaderprofile
        return CreateView.form_valid(self, form)
    
    def get_success_url(self):
        return reverse('browse', args=(self.object.name,))