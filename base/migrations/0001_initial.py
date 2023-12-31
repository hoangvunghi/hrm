# Generated by Django 4.2.7 on 2023-12-16 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('UserID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('UserStatus', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('EmpID', models.IntegerField(primary_key=True, serialize=False)),
                ('EmpName', models.CharField(max_length=255)),
                ('Phone', models.CharField(max_length=15)),
                ('HireDate', models.DateTimeField()),
                ('BirthDate', models.DateTimeField()),
                ('Address', models.CharField(max_length=255)),
                ('PhotoPath', models.CharField(max_length=255)),
                ('Email', models.EmailField(max_length=254)),
                ('EmpStatus', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('proj_id', models.AutoField(primary_key=True, serialize=False)),
                ('proj_name', models.CharField(max_length=20)),
                ('proj_value', models.IntegerField()),
                ('date_start', models.DateField(auto_now=True)),
                ('date_end', models.DateField()),
                ('proj_description', models.CharField(max_length=200)),
                ('complete', models.CharField(choices=[('finished', 'Finished'), ('unfinished', 'Unfinished')], default='unfinished', max_length=20)),
                ('manager_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('proj_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.employee')),
            ],
        ),
    ]
