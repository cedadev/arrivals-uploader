from django.core.files.storage import FileSystemStorage
from django.conf import settings


class ArrivalsStorage(FileSystemStorage):

    def __init__(self, **kwargs):

        if "location" in kwargs:
            kwargs.pop("location")
        super().__init__(location=settings.USERS_DIR, **kwargs)
