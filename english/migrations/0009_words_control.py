# Generated by Django 3.1.2 on 2021-11-05 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0008_wordparams_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='words',
            name='control',
            field=models.BooleanField(default=False),
        ),
    ]
