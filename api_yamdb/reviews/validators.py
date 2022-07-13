import datetime
from django.core.exceptions import ValidationError


def year_validation(year):
    """Валидация года произведения"""
    if year > datetime.datetime.now().year:
        raise ValidationError('Год не может быть больше текущего!')


def validate_score(score):
    """Валидатор поля для оценки"""
    if score < 1 or score > 10:
        raise ValidationError(f'Оценка может быть от 1 до 10!',
                              code='false range',
                              params={'score': score}
                              )
