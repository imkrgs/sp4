from django.db import models

# Create your models here.


class request_project(models.Model):
    projectId = models.BigIntegerField()
    username = models.CharField(max_length=100)
    tsm = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='pending')
