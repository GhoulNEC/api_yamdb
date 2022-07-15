# API YaMDb
***

## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку. Из пользовательских оценок формируется рейтинг.
***
## Технологии
* Python 3.8.9
* Django 2.2.16
* djangorestframework 3.12.4

С полным списком технологий можно ознакомиться в файле requirements.txt
***
## Документация
С документацией проекта можно ознакомиться по [ссылке](http://127.0.0.1:8000/redoc/) после запуска проекта.
***
## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/GhoulNEC/api_yambd.git
```

```
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
***
## Авторы
* [Вячеслав Наприенко](https://github.com/Hellon048)
* [Максим Игнатов](https://github.com/Maxon57)
* [Роман Евстафьев](https://github.com/GhoulNEC)