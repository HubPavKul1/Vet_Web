# Generated by Django 4.2.4 on 2023-08-24 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_companies', '0004_alter_employee_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='slug',
        ),
    ]
