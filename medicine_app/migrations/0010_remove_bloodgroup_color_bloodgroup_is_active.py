# Generated by Django 5.1.5 on 2025-02-11 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine_app', '0009_bloodgroup_createuser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodgroup',
            name='color',
        ),
        migrations.AddField(
            model_name='bloodgroup',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Нажата'),
        ),
    ]
