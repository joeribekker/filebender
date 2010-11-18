from string import hexdigits
from random import choice

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage


storage = FileSystemStorage(location=settings.STORAGE_ROOT,
                            base_url=settings.STORAGE_URL)


def secret_generator(size=settings.FILE_SECRET_LENGTH):
    return "".join([choice(hexdigits) for i in range(size)])


class BigFile(models.Model):
    data = models.FileField(storage=storage, upload_to='shit')
    expire_date = models.DateTimeField()
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    message = models.TextField(blank=True)
    secret = models.CharField(max_length=settings.FILE_SECRET_LENGTH,
                              default=secret_generator)
    
    def __unicode__(self):
        return self.data.name

    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)


class Downloader(models.Model):
    file = models.ForeignKey(File, related_name="downloaders")
    email = models.EmailField()

    def __unicode__(self):
        return self.email