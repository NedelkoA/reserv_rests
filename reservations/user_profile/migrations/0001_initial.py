# Generated by Django 2.1 on 2018-08-21 08:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status_user', models.CharField(choices=[('usr', 'Client'), ('rst_adm', 'Restaurant admin')], default='usr', max_length=20)),
                ('telephone', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^\\+380\\d{9}$', "Phone number must be entered in the format: '+380xxxxxxxxx'.")])),
            ],
        ),
    ]
