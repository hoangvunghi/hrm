# Generated by Django 4.2.7 on 2023-11-27 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_useraccount_date_of_hire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='check_in_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]