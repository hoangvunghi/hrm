# Generated by Django 4.2.7 on 2024-01-08 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_employee_depid_alter_employee_jobid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='Bank',
            new_name='BankName',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='BankBranch',
        ),
    ]
