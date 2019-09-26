""" Views related to browsing. """

__author__ = "William Tucker"
__date__ = "2018-03-13"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView

from uploader.utils.streams import get_streams, get_stream
from uploader.forms import UploadForm
from uploader.decorators import data_directory_required
from uploader.models.stream import Stream


@method_decorator(data_directory_required, name='dispatch')
class BrowseView(TemplateView):
    
    template_name = 'uploader/browse.html'
    success_url = reverse_lazy('browse')
    
    def get_context_data(self, **kwargs):
        
        streams, unknown_streams = get_streams(
            self.request.user, include_unknown=True)
        
        # Sort by name
        streams.sort(key=lambda x: x.name)
        
        context = super(BrowseView, self).get_context_data(**kwargs)
        context.update({
            "streams": streams,
            "unknown_streams": unknown_streams,
        })
        
        return context


@method_decorator(data_directory_required, name='dispatch')
class BrowseStreamView(TemplateView, FormView):
    
    template_name = 'uploader/browse_stream.html'
    success_url = reverse_lazy('stream')
    form_class = UploadForm
    
    def get_form_kwargs(self):
        
        kwargs = super().get_form_kwargs()
        kwargs.update(self.kwargs)
        kwargs.update({'request': self.request})
        return kwargs
    
    def form_valid(self, form):
        
        return render(self.request,
                      self.template_name,
                      self.get_context_data(form.stream, form.rel_dir))
    
    def form_invalid(self, form):
        
        return render(self.request,
                      self.template_name,
                      self.get_context_data(form.stream, form.rel_dir, form=form))
    
    def get(self, request, stream, *args, **kwargs):
        
        stream_object = get_stream(self.request.user, stream)
        if not stream_object:
            return redirect('browse')
        
        return render(request, self.template_name, self.get_context_data(stream_object, *args, **kwargs))

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        
        if form.is_valid():
            for uploaded_file in files:
                self.write_file(request, form, uploaded_file)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_context_data(self, stream, rel_dir=None, form=None, **kwargs):
        
        context = super(BrowseStreamView, self).get_context_data(**kwargs)

        if isinstance(stream, str):
            stream = get_stream(self.request.user, stream)

        is_unknown = not isinstance(stream, Stream)

        arrivals_dir = self.request.user.uploaderprofile.data_directory
        browse_dir = os.path.join(arrivals_dir, stream.name)
        if rel_dir:
            browse_dir = os.path.join(browse_dir, rel_dir)
        
        parent = None if not rel_dir else os.path.dirname(rel_dir)
        
        context.update({
            "browse_dir": browse_dir,
            "rel_dir": rel_dir,
            "stream": stream,
            "parent": parent,
            "is_unknown": is_unknown,
        })
        return context

    @staticmethod
    def write_file(request, form, uploaded_file):

        data_directory = request.user.uploaderprofile.data_directory

        if form.stream:
            rel_dir = '' if form.rel_dir == None else form.rel_dir
            rel_dir = rel_dir.strip('/')
            
            new_file_path = os.path.join(data_directory, form.stream, rel_dir, uploaded_file.name)
            
            if os.path.abspath(new_file_path).startswith(data_directory):
                
                # Write data
                with open(new_file_path, 'wb+') as new_file:
                    for chunk in uploaded_file.chunks():
                        new_file.write(chunk)
