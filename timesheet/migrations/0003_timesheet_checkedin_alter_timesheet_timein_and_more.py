# Generated by Django 4.2.7 on 2024-01-04 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0002_alter_timesheet_timeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='CheckedIn',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='TimeIn',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='TimeOut',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
