from django.contrib import admin

from .models import *
from app_animals.models import Animal


class AnimalInline(admin.TabularInline):
    model = Animal
    row_id_fields = ['company']
    extra = 0


class StreetInline(admin.TabularInline):
    model = Street
    row_id_fields = ['city']
    extra = 0


class EmployeeInline(admin.TabularInline):
    model = Employee
    row_id_fields = ['company']
    extra = 0


class AddressInline(admin.TabularInline):
    model = Address
    row_id_fields = ['street', 'company']
    extra = 0


# class PositionInline(admin.TabularInline):
#     model = Position
#     row_id_fields = ['company']
#     extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name", )}
    inlines = [EmployeeInline, AddressInline, AnimalInline]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [StreetInline]


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass





