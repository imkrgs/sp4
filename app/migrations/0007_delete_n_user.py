# Generated by Django 4.1.2 on 2022-11-22 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_n_user_password1_remove_n_user_password2_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='N_user',
        ),
    ]