from django.db import models

from django.contrib.auth.models import User


class File(models.Model):
    # TODO: use custom storage system
    # http://docs.djangoproject.com/en/dev/howto/custom-file-storage/
    data = models.FileField(upload_to="incomming")
    expire_date = models.DateTimeField()
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    message = models.TextField(blank=True)
    #secret = models.CharField(50)
    
    def __unicode__(self):
        return self.data.name




class Downloader(models.Model):
    file = models.ForeignKey(File)
    email = models.EmailField()
