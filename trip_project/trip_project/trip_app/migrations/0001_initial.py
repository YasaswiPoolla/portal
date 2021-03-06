# Generated by Django 3.0.7 on 2020-07-12 12:14

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import trip_project.trip_app.model_managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('user_sqn', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(db_column='firstname', max_length=50)),
                ('last_name', models.CharField(db_column='lastname', max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(db_column='mobile', max_length=20)),
                ('last_login', models.DateTimeField(auto_now_add=True, db_column='last_login')),
                ('is_active', models.BooleanField(db_column='isActive', default=False)),
                ('profile_image', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', trip_project.trip_app.model_managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserException',
            fields=[
                ('exception_sqn', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_request', django.contrib.postgres.fields.jsonb.JSONField()),
                ('stack_trace', models.TextField()),
                ('log_datetime', models.DateTimeField(auto_now_add=True, db_column='logDateTime')),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(db_column='user_sqn', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('trip_sqn', models.BigAutoField(primary_key=True, serialize=False)),
                ('from_location', models.CharField(db_column='fromlocation', max_length=50)),
                ('to_location', models.CharField(db_column='tolocation', max_length=50)),
                ('trip_date', models.DateTimeField(auto_now_add=True, db_column='tripdate')),
                ('trip_distance', models.BigIntegerField(db_column='tripdistance', null=True)),
                ('user', models.ForeignKey(db_column='user_sqn', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TripImages',
            fields=[
                ('images_sqn', models.BigAutoField(primary_key=True, serialize=False)),
                ('images', models.FileField(blank=True, null=True, upload_to='memories')),
                ('trip', models.ForeignKey(db_column='trip_sqn', on_delete=django.db.models.deletion.PROTECT, to='trip_app.Trips')),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_sqn', models.BigAutoField(primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_column='at_location', null=True)),
                ('location_name', models.CharField(db_column='locationname', max_length=50)),
                ('trip', models.ForeignKey(db_column='trip_sqn', on_delete=django.db.models.deletion.PROTECT, to='trip_app.Trips')),
            ],
        ),
    ]
