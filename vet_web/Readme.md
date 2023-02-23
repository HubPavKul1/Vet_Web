# Vet_Web.
## Веб приложение для учета ветеринарной работы на django.

### УСТАНОВКА:
* Клонируйте репозиторий в свою виртуальную среду окружения git clone 
```.env
git clone https://github.com/HubPavKul1/Vet_Web.git
```
* Установите необходимые зависимости из файла requirements.txt
```.env
pip install -r requirements.txt
```
* Примените миграции 
```.env
python manage.py makemigrations 
python manage.py migrate
```
* Запустите сервер командой 
```.env
python manage.py runserver
```
* Пройдите по ссылке для ознакомления с документацией проекта
http://127.0.0.1:8000/swagger/ 