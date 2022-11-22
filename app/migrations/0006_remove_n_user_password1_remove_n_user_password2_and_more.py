# Generated by Django 4.1.1 on 2022-11-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_project_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='n_user',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='n_user',
            name='password2',
        ),
        migrations.AlterField(
            model_name='n_user',
            name='role',
            field=models.CharField(choices=[('User', 'User'), ('TSM', 'TSM')], default='User', max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('Reject', 'Reject'), ('Approved', 'Approved')], default='pending', max_length=50),
        ),
    ]