from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    screenshot = models.FileField(upload_to='media')
    source = models.FileField(upload_to='media')
    user_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='pending',choices=[('pending', 'pending'), ('Reject', 'Reject'),('Approved', 'Approved')])
