# Generated by Django 4.1.3 on 2023-01-29 22:02

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_title', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
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
                ('slug', models.SlugField(blank=True, null=True)),
                ('mobile', models.CharField(help_text='<em>10 digits</em>', max_length=12, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('pax', models.PositiveSmallIntegerField(default=1)),
                ('source', models.CharField(choices=[('whatsapp', 'WhatsApp'), ('email', 'Email'), ('phone', 'Phone'), ('founder', 'Founder'), ('socialm', 'Social Media'), ('web', 'Website'), ('other', 'Other')], max_length=10)),
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
                ('slug', models.SlugField(blank=True, null=True)),
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
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
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
                ('transfers', models.CharField(blank=True, choices=[('PB-HV-PB-ALL', 'PB-HV AI'), ('PB-HV-NL-PB-ALL', 'PB-HV-NL AI'), ('PB-HV-PB-PnD', 'PB-HV P-n-D'), ('PB-HV-NL-PB-PnD', 'PB-HV-NL P-n-D'), ('PB-HV-Ferry', 'Ferry-Only-PB-HV'), ('PB-HV-NL-Ferry', 'Ferry-Only-PB-HV-NL')], max_length=21, null=True)),
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
                ('hotel_hv', models.ForeignKey(blank=True, limit_choices_to={'location_id': 2}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hv_hotel_set', to='gobasic.hotel', verbose_name='Hotel Havelock')),
                ('hotel_nl', models.ForeignKey(blank=True, limit_choices_to={'location_id': 3}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nl_hotel_set', to='gobasic.hotel', verbose_name='Hotel Neil')),
                ('hotel_pb', models.ForeignKey(blank=True, limit_choices_to={'location': 'port blair'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pb_hotel_set', to='gobasic.hotel', verbose_name='Hotel Port Blair')),
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
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_owner', models.BooleanField(default=False, verbose_name='Is Owner ?')),
                ('is_manager', models.BooleanField(default=False, verbose_name='Is Manager ?')),
                ('is_employee', models.BooleanField(default=False, verbose_name='Is Employee ?')),
                ('is_intern', models.BooleanField(default=False, verbose_name='Is Intern ?')),
                ('is_customer', models.BooleanField(default=False, verbose_name='Is Customer ?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
