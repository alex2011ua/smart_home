# Generated by Django 3.1.2 on 2021-06-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_auto_20210602_1548"),
    ]

    operations = [
        migrations.AddField(
            model_name="params",
            name="max_temp_teplica",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="params",
            name="min_temp_teplica",
            field=models.IntegerField(null=True),
        ),
    ]
