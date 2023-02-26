from django.db import models
from django.urls import reverse


class City(models.Model):
    """ Модель Город"""
    name = models.CharField(max_length=255, verbose_name='город', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'
        verbose_name = 'city'
        verbose_name_plural = 'cities'


class Street(models.Model):
    """ Модель Улица """
    city = models.ForeignKey(City,
                             verbose_name='город',
                             on_delete=models.CASCADE,
                             related_name='streets')
    name = models.CharField(max_length=255,
                            verbose_name='улица',
                            blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'streets'
        verbose_name = 'street'
        verbose_name_plural = 'streets'


class Company(models.Model):
    """ Модель Предприятие """
    full_name = models.CharField(max_length=255,
                                 verbose_name='полное наименование',
                                 blank=True)
    short_name = models.CharField(max_length=255,
                                  verbose_name='сокращенное наименование',
                                  blank=True)
    slug = models.SlugField(max_length=255,
                            verbose_name='url',
                            help_text='unique url fragment based on the company short_name'
                            )
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'companies'
        verbose_name = 'company'
        verbose_name_plural = 'companies'


class Address(models.Model):
    """ Модель адрес """
    street = models.ForeignKey(Street,
                               verbose_name='улица',
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='address')
    company = models.ForeignKey(Company,
                                verbose_name='предприятие',
                                null=True, on_delete=models.CASCADE,
                                related_name='address')
    house_number = models.CharField(max_length=10,
                                    verbose_name='номер дома',
                                    blank=True)
    phone_number_1 = models.CharField(max_length=12,
                                      verbose_name='телефон 1',
                                      blank=True)
    phone_number_2 = models.CharField(max_length=12,
                                      verbose_name='телефон 1',
                                      blank=True)

    def __str__(self):
        return f'{self.street}, {self.house_number}'

    class Meta:
        db_table = 'address'
        verbose_name = 'address'
        verbose_name_plural = 'address'


class Position(models.Model):
    """ Модель должность работника """
    name = models.CharField(max_length=100, verbose_name='должность', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'positions'
        verbose_name = 'position'
        verbose_name_plural = 'positions'


class Employee(models.Model):
    """ Модель сотрудник предприятия """
    company = models.ForeignKey(Company,
                                verbose_name='предприятие',
                                on_delete=models.CASCADE,
                                related_name='positions',
                                null=True
                                )
    position = models.ForeignKey(Position,
                                 verbose_name='должность',
                                 on_delete=models.CASCADE,
                                 related_name='employees')

    last_name = models.CharField(max_length=255,
                                 verbose_name='фамилия',
                                 blank=True)
    first_name = models.CharField(max_length=255,
                                  verbose_name='имя',
                                  blank=True)
    patronymic = models.CharField(max_length=255,
                                  verbose_name='отчество',
                                  blank=True)
    full_name = models.CharField(max_length=200, verbose_name='ФИО', blank=True)  # автозаполнение из предыдущих полей
    available = models.BooleanField(default=True)

    slug = models.SlugField(max_length=255,
                            verbose_name='url',
                            help_text='unique url fragment based on the employee full_name'
                            )

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'employees'
        verbose_name = 'employee'
        verbose_name_plural = 'employees'
