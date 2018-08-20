from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Restaurant(models.Model):
    title = models.CharField(max_length=64)
    number_tables = models.IntegerField(validators=[
        MinValueValidator(5)
    ])

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'

    def __str__(self):
        return self.title


class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    table = models.IntegerField()
    visitors = models.IntegerField(
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
        models.CASCADE,
        related_name='reservations'
    )


class UserProfile(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    telephone = models.CharField(
        max_length=13,
        validators=[
            RegexValidator('^\+380\d{9}$',
                           'Phone number must be entered in the format: \'+380xxxxxxxxx\'.')
        ]
    )

    def __str__(self):
        return self.user.username

