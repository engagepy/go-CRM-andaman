# Generated by Django 4.1.3 on 2022-11-04 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobasic', '0018_trip_activity_cost_alter_trip_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='activity_cost',
        ),
    ]