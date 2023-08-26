from django.db import models
from app_companies.models import Company


class TypeOfFeeding(models.Model):
    """Модель Тип питания животного"""
    name = models.CharField(max_length=50,
                            verbose_name='тип питания',
                            help_text='тип питания животного'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'types_of_feeding'
        verbose_name = 'type_of_feeding'
        verbose_name_plural = 'types_of_feeding'
        ordering = ('name',)


class AnimalGroup(models.Model):
    """Модель Группа животных"""
    name = models.CharField(max_length=50,
                            verbose_name='группа животных'
                            )
    type_of_feeding = models.ForeignKey(TypeOfFeeding,
                                        verbose_name='тип питания',
                                        on_delete=models.CASCADE,
                                        null=True,
                                        related_name='animals'
                                        )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'animal_groups'
        verbose_name = 'animal_group'
        verbose_name_plural = 'animal_groups'
        ordering = ('name',)


class Species(models.Model):
    """Модель Вид животного"""
    name = models.CharField(max_length=50,
                            verbose_name='вид животного'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'species'
        verbose_name = 'species'
        verbose_name_plural = 'species'
        ordering = ('name',)


class TypeOfUse(models.Model):
    """Модель Тип использования животного"""
    name = models.CharField(max_length=50,
                            verbose_name='тип использования'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'types_of_use'
        verbose_name = 'type_of_use'
        verbose_name_plural = 'types_of_use'
        ordering = ('name',)


class AnimalSex(models.Model):
    """Модель Пол животного"""
    name = models.CharField(max_length=50,
                            verbose_name='пол животного'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'animals_sex'
        verbose_name = 'animal_sex'
        verbose_name_plural = 'animals_sex'
        ordering = ('name',)


class Animal(models.Model):
    """Модель Животное"""
    company = models.ForeignKey(Company,
                                verbose_name='предприятие',
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='animals'
                                )
    animal_group = models.ForeignKey(AnimalGroup,
                                     verbose_name='группа животных',
                                     on_delete=models.CASCADE,
                                     null=True,
                                     related_name='animals'
                                     )
    species = models.ForeignKey(Species,
                                verbose_name='вид животного',
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='animals'
                                )
    type_of_use = models.ForeignKey(TypeOfUse,
                                    verbose_name='тип использования',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    related_name='animals'
                                    )
    sex = models.ForeignKey(AnimalSex,
                            verbose_name='пол животного',
                            on_delete=models.CASCADE,
                            null=True,
                            related_name='animals'
                            )
    nickname = models.CharField(max_length=255,
                                verbose_name='кличка',
                                blank=True
                                )
    date_of_birth = models.DateField(verbose_name='дата рождения')
    identification = models.CharField(max_length=25,
                                      verbose_name='идентификация',
                                      blank=True
                                      )
    available = models.BooleanField(verbose_name='в наличии',
                                    default=True
                                    )

    def __str__(self):
        return f'{self.species} {self.sex} {self.nickname} {self.date_of_birth}'

    class Meta:
        db_table = 'animals'
        verbose_name = 'animal'
        verbose_name_plural = 'animals'
        ordering = ('animal_group', 'species', 'nickname',)

