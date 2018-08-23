from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Restaurant(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='articles',
        default=None
    )
    title = models.CharField(max_length=64)
    number_tables = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(5)]
    )
    open_time = models.CharField(max_length=5)
    close_time = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'

    def __str__(self):
        return self.title


class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    table = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visitors = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )
    contact_telephone = models.CharField(
        max_length=13,
        validators=[
            RegexValidator('^\+380\d{9}$',
                           'Phone number must be entered in the format: \'+380xxxxxxxxx\'.')
        ]
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    def __str__(self):
        return self.restaurant.title + ' ' + str(self.date)


class Table(models.Model):
    numb = models.PositiveSmallIntegerField()
    count_sits = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2)]
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.restaurant.title + str(self.numb)
