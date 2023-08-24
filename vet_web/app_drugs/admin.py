from django.contrib import admin
from .models import *


# class DrugInline(admin.TabularInline):
#     model = Drug
#     row_id_fields = ['drug_manufacturer']
#     extra = 0


class DrugInMovementInline(admin.TabularInline):
    model = DrugInMovement
    row_id_fields = ['drug']
    extra = 0


@admin.register(DrugManufacturer)
class DrugManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountingUnit)
class AccountingUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Dosage)
class DosageAdmin(admin.ModelAdmin):
    pass


@admin.register(AdministrationMethod)
class AdministrationMethod(admin.ModelAdmin):
    pass


@admin.register(PlaceOfAdministration)
class PlaceOfAdministration(admin.ModelAdmin):
    pass


@admin.register(DrugMovement)
class DrugMovement(admin.ModelAdmin):
    inlines = [DrugInMovementInline]


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    pass


@admin.register(DrugInMovement)
class DrugInMovementAdmin(admin.ModelAdmin):
    pass

