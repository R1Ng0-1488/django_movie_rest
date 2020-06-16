from django.db import models
from datetime import date
from django.shortcuts import reverse
# Create your models here.


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=200)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актеры и Режиссеры"""
    name = models.CharField('Имя', max_length=200)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie:actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = 'Актер или Режиссер'
        verbose_name_plural = 'Актеры и Режиссеры'


class Genre(models.Model):
    """Жанры"""
    name = models.CharField('Имя', max_length=200)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movies(models.Model):
    """Фильмы"""
    title = models.CharField('Название', max_length=200)
    tagline = models.CharField('Слоган', max_length=200, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='posters/')
    year = models.PositiveSmallIntegerField('Год', default=2020)
    country = models.CharField('Страна', max_length=30)
    trailer = models.URLField('Трейлер', blank=True)
    directors = models.ManyToManyField(
        Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actors')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', related_name='film_genre')
    world_premiere = models.DateField('Мировая примьера', default=date.today)
    usa_premiere = models.DateField('Примьера в США', default=date.today)
    budget = models.PositiveIntegerField(
        'Бюджет', default=0, blank=True, help_text='Указать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(
        'Сборы в США', default=0, blank=True, help_text='Указать сумму в долларах')
    fees_in_world = models.PositiveIntegerField(
        'Сборы в мире', default=0, blank=True, help_text='Указать сумму в долларах')
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def get_absolute_url(self):
        return reverse('movie:movie_detail', kwargs={'slug': self.url})

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ('-id',)


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movies, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильм'
        verbose_name_plural = 'Кадры из фильмов'


class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name_plural = 'Звезда рейтинга'
        verbose_name = 'Звезды рейтинга'
        ordering = ["value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField('IP адресс', max_length=15)
    star = models.ForeignKey(
        RatingStar, verbose_name='Звезды рейтинга', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, verbose_name='Фильм', on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return '{0} - {1}'.format(self.star, self.movie)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField('Имя', max_length=150)
    message = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Родитель', related_name='children')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, verbose_name='Фильм', related_name='reviews')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
