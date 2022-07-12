from django.core.exceptions import ValidationError
from django.db import models
from core.models import CreatedModel


def validate_score(score):
    """Валидатор поля для оценки"""
    if score < 1 or score > 10:
        raise ValidationError(f'Оценка может быть от 1 до 10!',
                              code='false range',
                              params={'score': score}
                              )


class Review(CreatedModel):
    """Создается модель с отзывами."""
    text = models.TextField('Отзыв',
                            help_text='Введите текст отзывы')
    score = models.ImageField('Оценка',
                              validators=[validate_score],
                              help_text='Введите оценку от 1 до 10')
    author = models.ForeignKey('User',
                               related_name='author',
                               on_delete=models.CASCADE,
                               verbose_name='Автор'
                               )
    titles = models.ForeignKey('Titles',
                               related_name='titles',
                               on_delete=models.CASCADE,
                               verbose_name='Произведение'
                               )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return '{0}: {1}'.format(
            self.author, self.titles.name
        )

    def save(self, *args, **kwargs):
        """Проверка пользователя на наличие отзыва."""
        if self.objects.filter(author=kwargs['author'],
                               titles=kwargs['titles']).exists():
            raise ValidationError('К сожалению, можно оставить только один отзыв',
                                  code='review error',
                                  params={'author': kwargs['author']}
                                  )
        return super().save(*args, **kwargs)


class Comments(CreatedModel):
    """Создается модель с комментариями."""
    text = models.TextField('Комментарий',
                            help_text='Введите комментарий'
                            )
    author = models.ForeignKey('User',
                               related_name='author',
                               on_delete=models.CASCADE,
                               verbose_name='Автор'
                               )
    review = models.ForeignKey(Review,
                               related_name='review',
                               on_delete=models.CASCADE,
                               verbose_name='Отзыв'
                               )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Отзыв к {0}: {1}'.format(
            self.review.pk, self.text
        )

