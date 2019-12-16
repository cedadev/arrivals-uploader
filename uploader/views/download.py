import os

from django_downloadview import StorageDownloadView


class ArrivalsStorageDownloadView(StorageDownloadView):
    """Serve file of storage by path.upper()."""

    stream_name_kwarg = "stream_name"

    def get_path(self):
        """Return uppercase path."""

        upload_path = self.request.user.uploaderprofile.upload_path
        stream_name = self.kwargs.get(self.stream_name_kwarg, None)

        path = super().get_path()
        path = os.path.join(upload_path, stream_name, path)

        return path
