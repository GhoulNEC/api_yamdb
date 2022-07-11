from django.db import models

from .validators import year_validation


class Categories(models.Model):
    name = models.CharField('Категория', max_length=120)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField('Жанр', max_length=150)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.TextField('Название произведения', max_length=150)
    year = models.IntegerField('Год выхода произведения',
                               validators=[year_validation], blank=True)
    description = models.TextField('Описание', max_length=300)
    genre = models.ManyToManyField(Genres, blank=True, related_name='titles')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='titles')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
