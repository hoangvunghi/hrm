# Generated by Django 4.2.7 on 2023-12-14 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_department_depid_alter_employee_empid_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='salaryhistory',
            name='unique_salary_history',
        ),
        migrations.AlterUniqueTogether(
            name='salaryhistory',
            unique_together={('EmpID', 'SalFrom')},
        ),
    ]