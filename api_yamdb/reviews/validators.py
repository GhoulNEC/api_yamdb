import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(year):
    now_year = dt.date.today()
    if year > now_year.year:
        raise ValidationError(f'Некорректный год {year}')
