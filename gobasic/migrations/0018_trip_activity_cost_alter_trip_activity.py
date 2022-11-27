# Generated by Django 4.1.3 on 2022-11-04 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gobasic', '0017_trip_transfer_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='activity_cost',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='trip',
            name='activity',
            field=models.ManyToManyField(blank=True, help_text='select multiple, note location tags', related_name='activity', to='gobasic.activity', verbose_name='Activities'),
        ),
    ]