# Generated by Django 3.1.2 on 2020-12-04 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_delete_christmas'),
    ]

    operations = [
        migrations.AddField(
            model_name='dht_mq',
            name='muve_kitchen',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
