# Generated by Django 3.1.5 on 2021-04-26 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210422_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.CharField(max_length=100)),
                ('venue_location', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('x_coord', models.FloatField(blank=True, null=True)),
                ('y_coord', models.FloatField(blank=True, null=True)),
                ('date_of_event', models.DateField()),
                ('description', models.CharField(max_length=200)),
                ('classification', models.CharField(choices=[('Infected', 'Infected'), ('Infector', 'Infector'), ('Both', 'Both')], default='Infected', max_length=10)),
                ('case_number_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.case')),
            ],
        ),
    ]
