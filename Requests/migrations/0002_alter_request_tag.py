# Generated by Django 4.1.4 on 2022-12-17 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Requests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='tag',
            field=models.CharField(default='PENDING', max_length=10, null=True),
        ),
    ]
