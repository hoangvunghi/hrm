# Generated by Django 4.2.7 on 2023-12-07 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=255)),
                ('tax_id', models.CharField(max_length=255)),
                ('number_of_employees', models.CharField(max_length=255)),
                ('registration_employees', models.CharField(max_length=255)),
                ('cost_center', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('tax', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('address_stress', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('zip_postalcode', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('note', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]