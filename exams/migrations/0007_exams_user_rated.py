# Generated by Django 4.1.4 on 2023-01-24 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exams', '0006_exams_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='exams',
            name='user_rated',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
