# Generated by Django 4.1.4 on 2023-01-25 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0009_alter_exams_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exams',
            name='user_rated',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
