# Generated by Django 3.1.2 on 2021-09-10 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WordParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learned', models.BooleanField(default=False)),
                ('heavy', models.BooleanField(default=False)),
                ('lesson_0', models.BooleanField(default=False)),
                ('lesson_1', models.BooleanField(default=False)),
                ('lesson_2', models.BooleanField(default=False)),
                ('lesson_3', models.BooleanField(default=False)),
                ('lesson_4', models.BooleanField(default=False)),
                ('lesson_5', models.BooleanField(default=False)),
                ('lesson_6', models.BooleanField(default=False)),
                ('lesson_7', models.BooleanField(default=False)),
                ('lesson_8', models.BooleanField(default=False)),
                ('lesson_9', models.BooleanField(default=False)),
                ('lesson_10', models.BooleanField(default=False)),
                ('lesson_11', models.BooleanField(default=False)),
                ('lesson_12', models.BooleanField(default=False)),
                ('lesson_13', models.BooleanField(default=False)),
                ('control_state', models.BooleanField(default=False)),
                ('irregular_verbs', models.BooleanField(default=False)),
                ('level_1', models.BooleanField(default=False)),

            ],
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english', models.CharField(max_length=128)),
                ('russian', models.CharField(max_length=128)),
                ('learned', models.BooleanField(default=False)),
                ('heavy', models.BooleanField(default=False)),
                ('info', models.CharField(blank=True, max_length=128)),
                ('lesson', models.PositiveIntegerField(blank=True, default=0)),
            ],
        ),
    ]
