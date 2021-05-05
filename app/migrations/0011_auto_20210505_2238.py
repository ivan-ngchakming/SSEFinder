# Generated by Django 3.1.5 on 2021-05-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
        migrations.AddField(
            model_name='classification',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]