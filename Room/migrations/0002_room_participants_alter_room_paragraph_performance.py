# Generated by Django 4.1.4 on 2022-12-23 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='participants',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='paragraph',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wpm', models.IntegerField(default=0, null=True)),
                ('cpm', models.IntegerField(default=0, null=True)),
                ('accuracy', models.IntegerField(default=0, null=True)),
                ('half_mistakes', models.IntegerField(default=0, null=True)),
                ('full_mistakes', models.IntegerField(default=0, null=True)),
                ('errors', models.IntegerField(default=0, null=True)),
                ('time_taken', models.IntegerField(default=0, null=True)),
                ('rank', models.IntegerField(default=0, null=True)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Room.room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]