# Generated by Django 3.1.2 on 2020-11-09 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Temp1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_temp', models.DateTimeField()),
                ('temp', models.IntegerField()),
                ('humidity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Temp_out',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dete_temp', models.DateTimeField()),
                ('temp', models.IntegerField()),
                ('humidity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WeatherRain',
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
