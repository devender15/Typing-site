# Generated by Django 4.1.4 on 2022-12-27 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0004_remove_performance_student'),
        ('UserAuthentication', '0006_user_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Room.room'),
        ),
    ]
