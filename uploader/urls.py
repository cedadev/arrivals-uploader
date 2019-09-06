""" URL Configuration for the app. """

__author__ = "William Tucker"
__date__ = "2017-07-28"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django.urls import path, re_path, include
from django.views.generic import RedirectView

from uploader.views import stream_views, browse_views, tool_views


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='browse', permanent=False)),

    # Stream views
    path('create/',
        stream_views.CreateStreamView.as_view(), name='create_stream'
    ),

    # Browse views
    path('browse/', browse_views.BrowseView.as_view(), name='browse'),
    path('browse/<stream>/',
        browse_views.BrowseStreamView.as_view(), name='browse'
    ),
    re_path('browse/(?P<stream>[\w\.-]+)/(?P<rel_dir>.*)/$',
        browse_views.BrowseStreamView.as_view(), name='browse'
    ),

    # Tool views
    path('delete/', tool_views.delete_file, name="delete"),
    path('mkdir/', tool_views.mkdir, name="mkdir"),
    path('rename/', tool_views.rename, name="rename"),
    path('fix_chars/', tool_views.fix_chars, name="fix_chars"),
    path('fix_remove_links/', tool_views.fix_links, name="fix_remove_links"),
    path('fix_zero_length/', tool_views.fix_zero, name="fix_zero_length"),
    path('fix_empty_dir/', tool_views.fix_empty, name="fix_empty_dir"),
    path('fix_unzip/', tool_views.fix_unzip, name="fix_unzip"),
    path('fix_delete_dir/', tool_views.fix_delete_dir, name="fix_delete_dir"),

    # Other upload methods
    path('ftp/', include('uploader.ftp.urls')),
    path('rsync/', include('uploader.rsync.urls')),
]
