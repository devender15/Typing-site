# Generated by Django 4.1.4 on 2023-01-05 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_alter_tests_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='tests',
            name='live',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
