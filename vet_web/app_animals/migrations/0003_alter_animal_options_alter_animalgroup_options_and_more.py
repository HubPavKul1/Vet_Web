# Generated by Django 4.2.4 on 2023-08-26 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_animals', '0002_alter_animal_animal_group_alter_animal_company_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animal',
            options={'ordering': ('animal_group', 'species', 'nickname'), 'verbose_name': 'animal', 'verbose_name_plural': 'animals'},
        ),
        migrations.AlterModelOptions(
            name='animalgroup',
            options={'ordering': ('name',), 'verbose_name': 'animal_group', 'verbose_name_plural': 'animal_groups'},
        ),
        migrations.AlterModelOptions(
            name='animalsex',
            options={'ordering': ('name',), 'verbose_name': 'animal_sex', 'verbose_name_plural': 'animals_sex'},
        ),
        migrations.AlterModelOptions(
            name='species',
            options={'ordering': ('name',), 'verbose_name': 'species', 'verbose_name_plural': 'species'},
        ),
        migrations.AlterModelOptions(
            name='typeoffeeding',
            options={'ordering': ('name',), 'verbose_name': 'type_of_feeding', 'verbose_name_plural': 'types_of_feeding'},
        ),
        migrations.AlterModelOptions(
            name='typeofuse',
            options={'ordering': ('name',), 'verbose_name': 'type_of_use', 'verbose_name_plural': 'types_of_use'},
        ),
    ]
