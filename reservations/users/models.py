from django.db import models

from main.models import Reservation, User


class UserReserve(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    reservations = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE
    )
    pre_order = models.BooleanField(
        null=True
    )
