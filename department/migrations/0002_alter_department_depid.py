# Generated by Django 4.2.7 on 2023-12-19 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='DepID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
