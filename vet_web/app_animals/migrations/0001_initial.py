# Generated by Django 4.2.4 on 2023-08-24 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_companies', '0004_alter_employee_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalSex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='пол животного')),
            ],
            options={
                'verbose_name': 'animal_sex',
                'verbose_name_plural': 'animals_sex',
                'db_table': 'animals_sex',
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='вид животного')),
            ],
            options={
                'verbose_name': 'species',
                'verbose_name_plural': 'species',
                'db_table': 'species',
            },
        ),
        migrations.CreateModel(
            name='TypeOfFeeding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='тип питания животного', max_length=50, verbose_name='тип питания')),
            ],
            options={
                'verbose_name': 'type_of_feeding',
                'verbose_name_plural': 'types_of_feeding',
                'db_table': 'types_of_feeding',
            },
        ),
        migrations.CreateModel(
            name='TypeOfUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='тип использования')),
            ],
            options={
                'verbose_name': 'type_of_use',
                'verbose_name_plural': 'types_of_use',
                'db_table': 'types_of_use',
            },
        ),
        migrations.CreateModel(
            name='AnimalGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='группа животных')),
                ('type_of_feeding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_animals.typeoffeeding', verbose_name='тип питания')),
            ],
            options={
                'verbose_name': 'animal_group',
                'verbose_name_plural': 'animal_groups',
                'db_table': 'animal_groups',
            },
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=255, verbose_name='кличка')),
                ('date_of_birth', models.DateField(verbose_name='дата рождения')),
                ('identification', models.CharField(blank=True, max_length=25, verbose_name='идентификация')),
                ('available', models.BooleanField(default=True, verbose_name='в наличии')),
                ('animal_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_animals.animalgroup', verbose_name='группа животных')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_companies.company', verbose_name='предприятие')),
                ('sex', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_animals.animalsex', verbose_name='пол животного')),
                ('species', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_animals.species', verbose_name='вид животного')),
                ('type_of_use', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_animals.typeofuse', verbose_name='тип использования')),
            ],
            options={
                'verbose_name': 'animal',
                'verbose_name_plural': 'animals',
                'db_table': 'animals',
            },
        ),
    ]