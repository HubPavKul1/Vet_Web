# Generated by Django 4.2.4 on 2023-08-24 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_companies', '0005_remove_employee_full_name_remove_employee_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_number_2',
            field=models.CharField(blank=True, max_length=12, verbose_name='телефон 2'),
        ),
    ]
