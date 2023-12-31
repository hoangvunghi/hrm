# Generated by Django 4.2.7 on 2023-12-19 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_employee_empid'),
        ('department', '0002_alter_department_depid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='EmpID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='base.employee'),
            preserve_default=False,
        ),
    ]
