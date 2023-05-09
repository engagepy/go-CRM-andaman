# Generated by Django 4.1.3 on 2023-03-02 00:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gobasic', '0002_alter_trip_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='profit_percentage',
            field=models.PositiveSmallIntegerField(default=11, help_text='Profit %', validators=[django.core.validators.MaxValueValidator(25), django.core.validators.MinValueValidator(7)], verbose_name='Profit %'),
        ),
    ]