# Generated by Django 2.2.7 on 2019-12-09 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IungoClientDashboard', '0007_auto_20191209_0632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useruploadsproject',
            name='user',
        ),
        migrations.AddField(
            model_name='design',
            name='design_number',
            field=models.CharField(default=1, max_length=10, verbose_name='Design Number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='project_number',
            field=models.CharField(default=1, max_length=10, verbose_name='project Number'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserUploads',
        ),
        migrations.DeleteModel(
            name='UserUploadsProject',
        ),
    ]
