# Generated by Django 4.2.7 on 2023-12-22 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0010_department_empid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='EmpID',
        ),
    ]