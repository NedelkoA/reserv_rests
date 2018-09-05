from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
    telegram_id = models.IntegerField(
        null=True,
        unique=True
    )

    def __str__(self):
        return self.user.username
