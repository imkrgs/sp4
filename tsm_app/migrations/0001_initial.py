# Generated by Django 4.1.1 on 2022-11-05 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='request_project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectId', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('tsm', models.CharField(max_length=100)),
                ('status', models.CharField(default='pending', max_length=50)),
            ],
        ),
    ]
