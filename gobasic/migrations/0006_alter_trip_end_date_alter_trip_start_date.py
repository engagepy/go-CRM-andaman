# Generated by Django 4.1.3 on 2022-11-01 22:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gobasic', '0005_alter_trip_end_date_alter_trip_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='trip',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='yyyy-mm-dd,hh--mm'),
        ),
    ]