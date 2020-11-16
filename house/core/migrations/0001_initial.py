# Generated by Django 3.1.2 on 2020-11-16 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DHT_MQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_t_h', models.DateTimeField()),
                ('temp_street', models.FloatField(null=True)),
                ('humidity_street', models.FloatField(null=True)),
                ('temp_voda', models.FloatField(null=True)),
                ('humidity_voda', models.FloatField(null=True)),
                ('temp_gaz', models.FloatField(null=True)),
                ('humidity_gaz', models.FloatField(null=True)),
                ('temp_teplica', models.FloatField(null=True)),
                ('humidity_teplica', models.FloatField(null=True)),
                ('temp_room', models.IntegerField(null=True)),
                ('humidity_room', models.IntegerField(null=True)),
                ('gaz_MQ4', models.IntegerField(null=True)),
                ('gaz_MQ135', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_log', models.DateTimeField()),
                ('title_log', models.CharField(max_length=50)),
                ('description_log', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('controller_name', models.CharField(max_length=40, unique=True)),
                ('label', models.CharField(max_length=100)),
                ('value', models.IntegerField(default=20)),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('rain', models.IntegerField(default=0)),
                ('temp_min', models.IntegerField(default=0)),
                ('temp_max', models.IntegerField(default=0)),
                ('snow', models.IntegerField(default=0)),
            ],
        ),
    ]
