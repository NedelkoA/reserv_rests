from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    status_user = models.CharField(
        default='usr',
        max_length=20, #delete
        choices=[
            ('usr', 'Client'),
            ('rst_adm', 'Restaurant admin')
        ]
    )
    telephone = models.CharField(
        max_length=13,
        validators=[
            RegexValidator('^\+380\d{9}$',
                           'Phone number must be entered in the format: \'+380xxxxxxxxx\'.')
        ]
    )

    def __str__(self):
        return self.user.username
