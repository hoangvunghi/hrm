# Generated by Django 4.2.7 on 2024-01-04 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0004_remove_timesheet_checkedin'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='data_dict',
            field=models.JSONField(default=dict),
        ),
    ]