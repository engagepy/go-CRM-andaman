# Generated by Django 4.1.3 on 2022-11-01 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobasic', '0003_alter_trip_acitivity_hv_alter_trip_acitivity_nl_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='acitivity_hv',
            new_name='activity_hv',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='acitivity_nl',
            new_name='activity_nl',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='acitivity_pb',
            new_name='activity_pb',
        ),
    ]