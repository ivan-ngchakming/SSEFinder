# Generated by Django 3.1.5 on 2021-05-05 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210504_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='identity_document_number',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]