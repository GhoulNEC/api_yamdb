import datetime
from django.core.exceptions import ValidationError


def year_validation(year):
    if year > datetime.datetime.now().year:
        raise ValidationError('Год не может быть больше текущего!')
