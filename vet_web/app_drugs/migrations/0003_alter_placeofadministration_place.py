# Generated by Django 4.2.4 on 2023-08-22 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_drugs', '0002_druginmovement_accounting_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeofadministration',
            name='place',
            field=models.CharField(blank=True, max_length=255, verbose_name='место введения препарата'),
        ),
    ]