# Generated by Django 4.2.7 on 2023-12-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_task_remove_project_useraccount_project_manager_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
