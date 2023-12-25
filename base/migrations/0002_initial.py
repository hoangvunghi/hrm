# Generated by Django 4.2.7 on 2023-12-16 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
        ('job', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='DepID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='JobID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.job'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='EmpID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.employee'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]