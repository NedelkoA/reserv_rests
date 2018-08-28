from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Restaurant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=64,
        unique=True
    )
    number_of_tables = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(5)]
    )
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'

    def __str__(self):
        return self.title


class Table(models.Model):
    table_number = models.PositiveSmallIntegerField()
    number_of_seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2)]
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            'table_number',
            'restaurant',
        )

    def __str__(self):
        return self.restaurant.title + ' #' + str(self.table_number)


class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    table = models.ForeignKey(
        Table,
        on_delete=models.DO_NOTHING
    )
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
    )

    def __str__(self):
        return self.restaurant.title + ' ' + str(self.date)
