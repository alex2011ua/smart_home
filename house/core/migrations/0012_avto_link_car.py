# Generated by Django 3.1.2 on 2022-02-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_avto'),
    ]

    operations = [
        migrations.AddField(
            model_name='avto',
            name='link_car',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
