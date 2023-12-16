# Generated by Django 4.2.7 on 2023-12-14 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_job_salaryhistory_remove_employee_posid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryhistory',
            name='SalID',
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='EmpID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.employee'),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='SalFrom',
            field=models.DateTimeField(primary_key=True, serialize=False),
        ),
    ]
