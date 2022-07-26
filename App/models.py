
from django.db import models

class searchResultDb(models.Model):
    search=models.CharField(max_length=100)
class searchperdayDb(models.Model):
    search=models.CharField(max_length=100)

class timeDb(models.Model):
    startedtime=models.DateTimeField(null=True,blank=False)
    endtime=models.DateTimeField(null=True,blank=False)

  