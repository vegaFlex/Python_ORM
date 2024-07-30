from django.db import models

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from main_app.mixins import AwardedMixin, UpdatedMixin
from main_app.menagers import DirectorManager


class Person(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50, default='Unknown')

    class Meta:
        abstract = True


class Director(Person):
    years_of_experience = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    objects = DirectorManager()


class Actor(Person, AwardedMixin, UpdatedMixin):
    pass


class Movie(AwardedMixin, UpdatedMixin):
    class MoviesGenre(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )

    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)

    genre = models.CharField(
        max_length=6,
        choices=MoviesGenre.choices,
        default=MoviesGenre.OTHER
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )

    is_classic = models.BooleanField(
        default=False
    )

    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='director_movies'
    )

    starring_actor = models.ForeignKey(
        Actor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        # related_name='starring_roles'
        related_name='starring_movies'
    )

    actors = models.ManyToManyField(Actor, related_name='movies')
