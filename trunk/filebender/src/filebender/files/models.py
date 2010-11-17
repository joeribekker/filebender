from string import hexdigits
from random import choice

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def secret_generator(size=settings.FILE_SECRET_LENGTH):
    return "".join([choice(hexdigits) for i in range(size)])

class File(models.Model):
    # TODO: use custom storage system
    # http://docs.djangoproject.com/en/dev/howto/custom-file-storage/
    data = models.FileField(upload_to="incomming")
    expire_date = models.DateTimeField()
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    message = models.TextField(blank=True)
    secret = models.CharField(max_length=settings.FILE_SECRET_LENGTH,
                              default=secret_generator)
    
    def __unicode__(self):
        return self.data.name

class Downloader(models.Model):
    file = models.ForeignKey(File, related_name="downloaders")
    email = models.EmailField()
