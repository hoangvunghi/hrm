# Generated by Django 4.2.7 on 2023-11-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_attendance_check_in_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(auto_now=True),
        ),
    ]