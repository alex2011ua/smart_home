# Generated by Django 3.1.2 on 2021-02-02 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("start", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="avto",
            old_name="value_int",
            new_name="USD",
        ),
        migrations.AddField(
            model_name="avto",
            name="foto",
            field=models.CharField(max_length=140, null=True),
        ),
    ]
