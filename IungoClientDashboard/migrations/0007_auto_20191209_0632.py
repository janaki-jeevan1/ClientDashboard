# Generated by Django 2.2.7 on 2019-12-09 06:32

import IungoClientDashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IungoClientDashboard', '0006_auto_20191209_0631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='design',
            name='design_images',
        ),
        migrations.AddField(
            model_name='design',
            name='design_images',
            field=models.FileField(blank=True, null=True, upload_to=IungoClientDashboard.models.content_file_name, verbose_name='Design Images'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_images',
        ),
        migrations.AddField(
            model_name='project',
            name='project_images',
            field=models.FileField(blank=True, null=True, upload_to=IungoClientDashboard.models.content_file_name, verbose_name='Project Images'),
        ),
    ]
