# Generated by Django 4.1.4 on 2022-12-27 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_alter_exams_attempts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tests',
            name='ratings',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
