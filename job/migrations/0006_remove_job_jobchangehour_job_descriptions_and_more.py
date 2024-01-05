# Generated by Django 4.2.7 on 2024-01-03 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0013_department_manageid'),
        ('job', '0005_alter_job_depid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='JobChangeHour',
        ),
        migrations.AddField(
            model_name='job',
            name='Descriptions',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job',
            name='DepID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.department'),
        ),
    ]