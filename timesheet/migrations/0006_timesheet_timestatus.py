# Generated by Django 4.2.7 on 2024-01-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0005_timesheet_data_dict'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='TimeStatus',
            field=models.CharField(default=None, max_length=100),
        ),
    ]