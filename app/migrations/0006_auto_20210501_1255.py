# Generated by Django 3.1.5 on 2021-05-01 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_event_sse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
