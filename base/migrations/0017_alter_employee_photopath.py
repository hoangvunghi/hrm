# Generated by Django 4.2.7 on 2024-01-08 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_rename_bank_employee_bankname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='PhotoPath',
            field=models.ImageField(default='employee_photos/default.jpg', upload_to='employee_photos/'),
        ),
    ]