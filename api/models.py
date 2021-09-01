from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser

from api.validators import year_validator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории',
                            help_text='Введите название категории',
                            max_length=200,
                            db_index=True)
    slug = models.SlugField(unique=True, default='default title')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Название жанра',
                            help_text='Введите название жанра',
                            max_length=200,
                            db_index=True)
    slug = models.SlugField(unique=True, default='default title')

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    year = models.PositiveIntegerField(
        default=2021,
        validators=[year_validator],
        blank=True,
        null=True,
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        symmetrical=False
    )

    def __str__(self):
        return self.name[:50]


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    score = models.IntegerField('Оценка',
                                default=1,
                                validators=[MaxValueValidator(10),
                                            MinValueValidator(1)])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               verbose_name='Автор отзыва')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')

    class Meta:
        ordering = ['-score']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария',
                               help_text='Комментарий автора')
    review = models.ForeignKey(Review, related_name='comments',
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class UserConfirmationCode(models.Model):
    confirmation_code = models.CharField('Confirmation code', max_length=50)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='confirm_code',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user',),
                name='unique_confirm_code'),
        )
