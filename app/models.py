from django.db import models

# Create your models here.

class N_user(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    # password1 = models.CharField(max_length=100)
    # password2 = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    role = models.CharField(max_length=100, default='User', choices=[('User', 'User'), ('TSM', 'TSM')])
    tsm = models.CharField(max_length=100, default='NONE')


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    screenshot = models.FileField(upload_to='media')
    source = models.FileField(upload_to='media')
    user_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='pending',choices=[('pending', 'pending'), ('Reject', 'Reject'),('Approved', 'Approved')])
