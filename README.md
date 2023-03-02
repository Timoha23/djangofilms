# Films collection
## Описание
Твоя коллекция фильмов на базе Django Framework.
Данная платформа позволяет пользователям добавлять фильмы в избранное, в смотреть позже и добавлять фильмы в список просмотренных с выставлением рейтинга. В проекте используется Kinopoisk Api Unofficial (https://kinopoiskapiunofficial.tech/).

## Использованные технологии

* Python 3.10.6;
* Django 3.2.16;
* kinopoisk-api-unofficial-client 2.2.2;
* SQLite.

## Возможности
* Создать собственную учетную запись;
* Искать фильмы/сериалы и т.п.;
* Добавлять фильмы в избранное;
* Добавлять фильмы в список "смотреть позже";
* Оценивать фильмы и добавлять в список просмотренных

## Как запустить проект:

- Склонируйте репозиторий на компьютер;
```
git clone https://github.com/Timoha23/djangofilms.git
```
- Установите виртуальное окружение;
```
python -m venv venv
```
- Активируйте виртуальное окружение;
```
source venv/Scripts/activate
```
- Установите зависимости из файла requirements.txt;
```
pip install -r requirements.txt
``` 
- Чтобы накатить миграции и запустить проект в папке с файлом manage.py выполните команды:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
