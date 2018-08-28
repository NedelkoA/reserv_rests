from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    status_user = models.CharField(
        default='usr',
        max_length=10,
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
        ],
        unique=True
    )

    def __str__(self):
        return self.user.username
