# Generated by Django 4.1.4 on 2022-12-27 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0005_remove_room_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='teacher',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
