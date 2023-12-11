# Generated by Django 4.2.7 on 2023-12-05 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_useraccount_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('proj_id', models.AutoField(primary_key=True, serialize=False)),
                ('proj_name', models.CharField(max_length=20)),
                ('proj_value', models.IntegerField()),
                ('date_start', models.DateField(auto_now=True)),
                ('date_end', models.DateField()),
                ('proj_description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('proj_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.project')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectManager',
            fields=[
                ('pm_id', models.AutoField(primary_key=True, serialize=False)),
                ('proj_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]