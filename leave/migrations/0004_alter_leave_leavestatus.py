# Generated by Django 4.2.7 on 2024-01-02 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_alter_leave_leaveenddate_alter_leave_leavestartdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='LeaveStatus',
            field=models.BooleanField(max_length=255),
        ),
    ]
