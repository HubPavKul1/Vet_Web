
def fill_street_table():
    with open('../app_companies/streets.txt', encoding='utf16') as f:
        for street in f:
            print(street.strip())
            # street_obj = Street(city=1, name=street)

