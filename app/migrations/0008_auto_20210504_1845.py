# Generated by Django 3.1.5 on 2021-05-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210501_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue_location',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
