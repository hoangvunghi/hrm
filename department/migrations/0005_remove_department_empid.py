# Generated by Django 4.2.7 on 2023-12-19 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0004_alter_department_empid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='EmpID',
        ),
    ]