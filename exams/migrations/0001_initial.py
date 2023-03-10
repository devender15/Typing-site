# Generated by Django 4.1.4 on 2022-12-17 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('attempts', models.IntegerField(blank=True, null=True)),
                ('added_on', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('attempts', models.IntegerField(blank=True, null=True)),
                ('ratings', models.IntegerField(blank=True, null=True)),
                ('teacher', models.CharField(blank=True, max_length=100, null=True)),
                ('institute', models.CharField(blank=True, max_length=100, null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exams')),
            ],
        ),
    ]
