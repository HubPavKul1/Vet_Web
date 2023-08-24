from django.db import models
from datetime import datetime

from app_vet_work.models import Disease


class DrugManufacturer(models.Model):
    """Модель Производитель препарата"""
    name = models.CharField(max_length=255,
                            verbose_name='производитель препарата',
                            blank=True
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'drug_manufacturers'
        verbose_name = 'drug_manufacturer'
        verbose_name_plural = 'drug_manufacturers'


class AccountingUnit(models.Model):
    """Модель Единица учета препарата"""
    name = models.CharField(max_length=30,
                            verbose_name='единица учета',
                            blank=True
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'accounting_units'
        verbose_name = 'accounting_unit'
        verbose_name_plural = 'accounting_units'


class Dosage(models.Model):
    """Модель Дозировка препарата"""
    dosage = models.TextField(verbose_name='дозировка препарата', blank=True)

    def __str__(self):
        return self.dosage

    class Meta:
        db_table = 'dosages'
        verbose_name = 'dosage'
        verbose_name_plural = 'dosages'


class AdministrationMethod(models.Model):
    """Модель Способ применения препарата"""
    name = models.CharField(max_length=20,
                            verbose_name='способ применения'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'administration_methods'
        verbose_name = 'administration_method'
        verbose_name_plural = 'administration_methods'


class PlaceOfAdministration(models.Model):
    """Модель Место введения препарата"""
    place = models.CharField(max_length=255,
                             verbose_name='место введения препарата',
                             blank=True
                             )

    def __str__(self):
        return self.place

    class Meta:
        db_table = 'place_of_administration'
        verbose_name = 'place_of_administration'
        verbose_name_plural = 'place_of_administration'


class Drug(models.Model):
    """Модель Препарат"""

    class Budget(models.TextChoices):
        Federal = 'Fed'
        Regional = 'Reg'
        Commercial = 'Com'

    disease = models.ForeignKey(Disease,
                                verbose_name='заболевание',
                                on_delete=models.CASCADE,
                                related_name='drugs',
                                help_text='ссылка на заболевание'
                                )
    name = models.CharField(max_length=255,
                            verbose_name='наименование препарата'
                            )
    drug_manufacturer = models.ForeignKey(DrugManufacturer,
                                          verbose_name='производитель препарата',
                                          on_delete=models.CASCADE,
                                          related_name='drugs',
                                          help_text='ссылка на производителя препарата'
                                          )
    budget = models.CharField(max_length=3,
                              choices=Budget.choices,
                              default=Budget.Federal
                              )
    image = models.ImageField(upload_to='drugs/images/')
    instruction = models.FileField(verbose_name='инструкция к препарату',
                                   upload_to='drugs/'
                                   )

    def __str__(self):
        return self.name


class DrugMovement(models.Model):
    class Operation(models.TextChoices):
        Receipt = 'поступление'
        Expense = 'расход'
        Destruction = 'уничтожение'

    operation = models.CharField(max_length=20,
                                 choices=Operation.choices,
                                 verbose_name='операция'
                                 )
    operation_date = models.DateField(verbose_name='дата операции',
                                      null=True,
                                      blank=True
                                      )

    def __str__(self):
        return f'{self.operation} {self.operation_date}'


class DrugInMovement(models.Model):
    """Модель Перемещаемый препарат"""
    drug_movement = models.ForeignKey(DrugMovement,
                                      verbose_name='вид перемещения',
                                      on_delete=models.CASCADE,
                                      related_name='drug_in_movement'
                                      )
    drug = models.ForeignKey(Drug,
                             verbose_name='препарат',
                             on_delete=models.CASCADE,
                             blank=True,
                             related_name='drugs_in_movement',
                             help_text='ссылка на модель препарат'
                             )

    batch = models.CharField(max_length=10,
                             verbose_name='серия',
                             blank=True
                             )
    control = models.CharField(max_length=10,
                               verbose_name='контроль',
                               blank=True
                               )
    production_date = models.DateField(verbose_name='дата выпуска',
                                       null=True,
                                       blank=True
                                       )
    expiration_date = models.DateField(verbose_name='срок годности',
                                       null=True,
                                       blank=True
                                       )
    accounting_unit = models.ForeignKey(AccountingUnit,
                                        verbose_name='единицы учета',
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True,
                                        related_name='drugs_in_movement'
                                        )
    packing = models.FloatField(verbose_name='фасовка',
                                null=True,
                                help_text='количество единиц учета в единице упаковки'
                                )
    packs_amount = models.PositiveSmallIntegerField(verbose_name='количество упаковок',
                                                    null=True
                                                    )
    units_amount = models.FloatField(verbose_name='количество единиц учета',
                                     null=True
                                     )
    available = models.BooleanField(verbose_name='в наличии',
                                    default=True
                                    )

    def __str__(self):
        return f'{self.drug.name} серия:{self.batch}'

    def is_expired(self) -> bool:
        current_date = datetime.today().date()
        if current_date > self.expiration_date:
            return False
        return True
