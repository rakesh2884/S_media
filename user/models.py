from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import validate_password
from s_media import settings


class User(AbstractUser):
    ROLES = (
        (1, 'User'),
        (2, 'Admin'),
        (3, 'Moderator'),
    )
    password = models.CharField(validators=[validate_password])
    role = models.CharField(max_length=20, choices=ROLES)
    profile_picture = models. \
        ImageField(upload_to=settings.UPLOAD_PROFILE_FOLDER,
                   null=True,
                   blank=True)
    followers = models.ManyToManyField('self',
                                       symmetrical=False,
                                       related_name='following')
    isLinksent = models.BooleanField(default=False)
    expired_time = models.IntegerField(null=True)

