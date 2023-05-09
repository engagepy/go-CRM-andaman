# Generated by Django 4.1.3 on 2023-03-02 07:56

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gobasic', '0003_trip_profit_percentage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transfer',
            options={'ordering': ['transfer_type']},
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='transfer_title',
        ),
        migrations.AddField(
            model_name='transfer',
            name='transfer_type',
            field=models.CharField(choices=[('All', 'All Inclusive'), ('Part', 'Partial'), ('Frac', 'Fractional')], default='All Inclusive', max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='customer_transfer', unique=True),
        ),
    ]
