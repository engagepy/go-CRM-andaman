# Generated by Django 4.1.3 on 2023-03-01 18:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_title', models.CharField(max_length=20, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='activity_title', unique=True)),
                ('acitivity_duration', models.CharField(choices=[('1H', '1 hour'), ('2H', '2 hour'), ('3H', '3 hour'), ('1D', '1 Day'), ('2D', '2 Day'), ('4D', '4 Day'), ('6D', '6 Day')], max_length=2)),
                ('description', models.CharField(max_length=250)),
                ('net_cost', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(1)])),
                ('activity_status', models.BooleanField(default=False)),
                ('entry_last_updated', models.DateTimeField(auto_now=True)),
                ('entry_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['activity_title'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
                ('mobile', models.CharField(help_text='<em>10 digits</em>', max_length=12, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('pax', models.PositiveSmallIntegerField(default=1)),
                ('source', models.CharField(choices=[('whatsapp', 'WhatsApp'), ('email', 'Email'), ('phone', 'Phone'), ('founder', 'Founder'), ('social', 'Social Media'), ('web', 'Website'), ('other', 'Other')], max_length=10)),
                ('entry_last_updated', models.DateTimeField(auto_now=True)),
                ('entry_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=25)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='hotel_name', unique=True)),
                ('customer_rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='1', max_length=1)),
                ('room_name', models.CharField(max_length=15)),
                ('room_categories', models.CharField(choices=[('Budget', 'Budget'), ('Premium', 'Premium'), ('Deluxe', 'Deluxe'), ('Luxury', 'Luxury'), ('Ultra Luxury', 'Ultra Luxury')], default='1', max_length=12)),
                ('net_cp', models.PositiveIntegerField(default=0, help_text='Per Day for 2pax', validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(1)], verbose_name='CP')),
                ('net_map', models.PositiveIntegerField(default=0, help_text='Per Day for 2pax', validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(1)], verbose_name='MAP')),
                ('net_cp_kid', models.PositiveIntegerField(default=0, help_text='Per Day for 1pax', validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(1)], verbose_name='CP Kid')),
                ('net_map_kid', models.PositiveIntegerField(default=0, help_text='Per Day for 1pax', validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(1)], verbose_name='MAP Kid')),
                ('entry_last_updated', models.DateTimeField(auto_now=True)),
                ('entry_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['customer_rating'],
            },
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='location', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_title', models.CharField(choices=[('All', 'All Inclusive'), ('Part', 'Partial'), ('Frac', 'Fractional')], max_length=20, unique=True, verbose_name='Type')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='transfer_title', unique=True)),
                ('Inclusions', models.CharField(max_length=250)),
                ('net_cost', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(1)])),
                ('entry_last_updated', models.DateTimeField(auto_now=True)),
                ('entry_created', models.DateTimeField(auto_now_add=True)),
                ('customer_transfer', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='gobasic.customer', verbose_name='Customer->Transfer')),
            ],
            options={
                'ordering': ['transfer_title'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('lead', models.CharField(blank=True, choices=[('Enquiry', 'Enquiry'), ('Proposal', 'Proposal'), ('Confirmed', 'Confirmed'), ('Passed', 'Passed'), ('VIP', 'VIP'), ('Defense', 'Defense'), ('F-n-F', 'F-n-F')], max_length=11, null=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, help_text='yyyy-mm-dd,hh--mm')),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('plan_pb', models.CharField(choices=[('net_cp', 'Breakfast'), ('net_map', 'Breakfast + 1 Meal')], default='CP', max_length=11, verbose_name='Meal Plan')),
                ('pb_rooms', models.PositiveSmallIntegerField(default=0, help_text='Number of Rooms', validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)], verbose_name='Port Blair Rooms')),
                ('pb_nights', models.PositiveSmallIntegerField(default=0, help_text='Port Blair Nights', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Port Blair Nights')),
                ('pb_add_on', models.PositiveBigIntegerField(default=0, help_text='Port Blair Hotel Add On', validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Port Blair Add-On')),
                ('plan_hv', models.CharField(choices=[('net_cp', 'Breakfast'), ('net_map', 'Breakfast + 1 Meal')], default='CP', max_length=11, verbose_name='Meal Plan')),
                ('hv_rooms', models.PositiveSmallIntegerField(default=0, help_text='Number of Rooms', validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)], verbose_name='Havelock Rooms')),
                ('hv_nights', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Havelock Nights')),
                ('hv_add_on', models.PositiveBigIntegerField(default=0, help_text='Havelock Hotel Add On', validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Havelock Hotel Add-On')),
                ('plan_nl', models.CharField(choices=[('net_cp', 'Breakfast'), ('net_map', 'Breakfast + 1 Meal')], default='CP', max_length=11, verbose_name='Meal Plan')),
                ('nl_rooms', models.PositiveSmallIntegerField(default=0, help_text='Number of Rooms', validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)], verbose_name='Neil Rooms')),
                ('nl_nights', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Neil Nights')),
                ('nl_add_on', models.PositiveBigIntegerField(default=0, help_text='Neil Hotel Add On', validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Neil Hotel Add-On')),
                ('duration', models.PositiveSmallIntegerField(blank=True, verbose_name='Trip Nights')),
                ('trip_completed', models.BooleanField(default=False)),
                ('transfer_cost', models.PositiveIntegerField(blank=True, default=0)),
                ('hotel_cost', models.PositiveIntegerField(default=0)),
                ('advance_paid', models.PositiveIntegerField(default=0)),
                ('activity_cost', models.PositiveIntegerField(default=0)),
                ('total_trip_cost', models.PositiveIntegerField(default=0)),
                ('profit', models.PositiveBigIntegerField(default=0)),
                ('tax', models.PositiveBigIntegerField(default=0)),
                ('booked', models.BooleanField(default=False)),
                ('entry_last_updated', models.DateTimeField(auto_now=True)),
                ('entry_created', models.DateTimeField(auto_now_add=True)),
                ('activities', models.ManyToManyField(blank=True, help_text='select multiple, note locations', related_name='activities', to='gobasic.activity')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gobasic.customer')),
                ('hotel_hv', models.ForeignKey(blank=True, limit_choices_to={'location': 'Havelock Island'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hv_hotel_set', to='gobasic.hotel', verbose_name='Hotel Havelock')),
                ('hotel_nl', models.ForeignKey(blank=True, limit_choices_to={'location': 'Neil Island'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nl_hotel_set', to='gobasic.hotel', verbose_name='Hotel Neil')),
                ('hotel_pb', models.ForeignKey(blank=True, limit_choices_to={'location': 'Port Blair'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pb_hotel_set', to='gobasic.hotel', verbose_name='Hotel Port Blair')),
                ('transfers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gobasic.transfer')),
            ],
            options={
                'ordering': [],
            },
        ),
        migrations.AddField(
            model_name='hotel',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gobasic.locations'),
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gobasic.locations'),
        ),
    ]