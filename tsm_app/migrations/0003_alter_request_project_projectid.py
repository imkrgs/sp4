# Generated by Django 4.1.1 on 2022-11-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tsm_app", "0002_alter_request_project_projectid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request_project",
            name="projectId",
            field=models.BigIntegerField(),
        ),
    ]