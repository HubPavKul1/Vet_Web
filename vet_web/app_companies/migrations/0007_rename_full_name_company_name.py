# Generated by Django 4.2.4 on 2023-08-26 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_companies', '0006_alter_address_phone_number_2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='full_name',
            new_name='name',
        ),
    ]
