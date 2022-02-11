import random
import os
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.utils import timezone


def filename_gen():
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    filename = ''
    for i in range(16):
        filename += random.choice(chars)
    return filename


def path_and_rename(instance, filename):
    upload_to = 'pictures'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    pic = models.ImageField(upload_to=path_and_rename, null=True, max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
