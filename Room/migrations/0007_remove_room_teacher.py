# Generated by Django 4.1.4 on 2022-12-27 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0006_room_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='teacher',
        ),
    ]