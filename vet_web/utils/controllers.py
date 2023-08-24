from vet_web.app_vet_work.models import Disease


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
