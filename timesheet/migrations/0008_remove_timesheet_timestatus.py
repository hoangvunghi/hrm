# Generated by Django 4.2.7 on 2024-01-11 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0007_alter_timesheet_timestatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='TimeStatus',
        ),
    ]
