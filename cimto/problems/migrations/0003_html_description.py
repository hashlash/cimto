# Generated by Django 4.1.4 on 2023-04-18 07:13

from django.db import migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_problem_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=django_bleach.models.BleachField(),
        ),
    ]
