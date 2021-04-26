# Generated by Django 3.1.5 on 2021-04-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('case_number', models.IntegerField(primary_key=True, serialize=False)),
                ('person_name', models.CharField(max_length=30)),
                ('identity_document_number', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('onset_date', models.DateField()),
                ('date_confirmed', models.DateField()),
            ],
        ),
    ]