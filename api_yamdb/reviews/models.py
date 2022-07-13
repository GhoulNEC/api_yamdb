from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel
from .validators import year_validation, validate_score

User = get_user_model()


class Category(models.Model):
    """Создается модель категорий."""
    name = models.CharField('Категория',
                            max_length=120,
                            db_index=True
                            )
    slug = models.SlugField(max_length=30,
                            unique=True,
                            db_index=True
                            )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Создается модель жанров."""
    name = models.CharField('Жанр',
                            max_length=150,
                            db_index=True
                            )
    slug = models.SlugField(max_length=30,
                            unique=True,
                            db_index=True
                            )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Создается модель произведений."""
    name = models.TextField('Название произведения',
                            max_length=150,
                            db_index=True
                            )
    year = models.IntegerField('Год выхода произведения',
                               validators=[year_validation],
                               blank=True)
    description = models.TextField('Описание',
                                   max_length=300
                                   )
    genre = models.ManyToManyField(Genre,
                                   through='TitlesGenre',
                                   blank=True
                                   )
    category = models.ForeignKey(Categorie,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 blank=True,
                                 null=True
                                 )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Смежная модель для жанров и произведений."""
    title = models.ForeignKey(Title,
                              related_name='genres',
                              on_delete=models.CASCADE
                              )
    genre = models.ForeignKey(Genre,
                              related_name='title',
                              on_delete=models.SET_NULL,
                              null=True,
                              )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(CreatedModel):
    """Создается модель с отзывами."""
    text = models.TextField('Отзыв',
                            help_text='Введите текст отзывы'
                            )
    score = models.IntegerField('Оценка',
                                validators=[validate_score],
                                help_text='Введите оценку от 1 до 10'
                                )
    author = models.ForeignKey(User,
                               related_name='reviews',
                               on_delete=models.CASCADE,
                               verbose_name='Автор'
                               )
    titles = models.ForeignKey(Title,
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


class Comment(CreatedModel):
    """Создается модель с комментариями."""
    text = models.TextField('Комментарий',
                            help_text='Введите комментарий'
                            )
    author = models.ForeignKey(User,
                               related_name='comments',
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
