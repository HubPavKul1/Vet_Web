from datetime import datetime, timedelta, date

import xlrd
from app_vet_work.models import Disease
from app_animals.models import Animal


def fill_street_table():
    with open('../app_companies/streets.txt', encoding='utf16') as f:
        for street in f:
            print(street.strip())
            # street_obj = Street(city=1, name=street)


def fill_disease_table():
    diseases = []
    with open('../app_vet_work/diseases.txt', encoding='utf8') as f:
        for disease in f:
            # print(disease.strip())
            disease_obj = Disease(name=disease)
            diseases.append(disease_obj)
    print(diseases)


class UploadAnimals(object):
    foreign_key_fields = ['company', 'animal_group', 'species', 'type_of_use', 'sex']
    model = Animal

    def __init__(self, data):
        data = data
        self.uploaded_file = data.get('file')
        self.parsing()

    def getting_related_model(self, field_name):
        related_model = self.model._meta.get_field(field_name).remote_field.model
        return related_model

    def getting_headers(self):
        sheet = self.sheet
        headers = dict()
        for column in range(sheet.ncols):
            value = sheet.cell(0, column).value
            headers[column] = value
        return headers

    def parsing(self):
        uploaded_file = self.uploaded_file
        work_book = xlrd.open_workbook(file_contents=uploaded_file.read())
        sheet = work_book.sheet_by_index(0)
        self.sheet = sheet

        headers = self.getting_headers()
        print(headers)

        animals_bulk_list = []
        for row in range(1, sheet.nrows):
            row_dict = {}
            for column in range(sheet.ncols):
                value = sheet.cell(row, column).value
                field_name = headers[column]

                if field_name == 'id' and not value:
                    continue

                if field_name == 'date_of_birth':
                    start = date(1900, 1, 1)
                    delta = timedelta(int(value)-2)
                    value = (start + delta).strftime("%Y-%m-%d")
                    print(value)

                if field_name in self.foreign_key_fields:
                    related_model = self.getting_related_model(field_name)
                    print(related_model)

                    instance, created = related_model.objects.get_or_create(name=value)
                    value = instance

                row_dict[field_name] = value
            print(row_dict)
            animals_bulk_list.append(Animal(**row_dict))
        Animal.objects.bulk_create(animals_bulk_list)

        return True



