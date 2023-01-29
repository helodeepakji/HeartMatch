from django.db import models
import datetime


# Create your models here.

class Chat(models.Model):
    username = models.CharField(max_length=50)
    chat = models.CharField(max_length=255)
    room = models.CharField(max_length=50)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.username

