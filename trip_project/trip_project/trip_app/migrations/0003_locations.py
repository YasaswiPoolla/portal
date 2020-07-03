# Generated by Django 3.0.7 on 2020-07-02 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0002_trips_trip_distance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_sqn', models.BigAutoField(primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('location_name', models.CharField(db_column='locationname', max_length=50)),
                ('trip', models.ForeignKey(db_column='trip_sqn', on_delete=django.db.models.deletion.PROTECT, to='trip_app.Trips')),
            ],
        ),
    ]