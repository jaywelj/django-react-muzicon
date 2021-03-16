from django_extensions.db.models import TimeStampedModel
from django.db import models

import string
import random


def generate_unique_code(length=6):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if not Room.objects.filter(code=code).exists():
            break

    return code


# Create your models here.
class Room(TimeStampedModel):
    code = models.CharField(
        max_length=8,
        default=generate_unique_code,
        unique=True,
    )
    host = models.CharField(
        max_length=50,
        unique=True,
    )
    guest_can_pause = models.BooleanField(
        default=False,
    )
    votes_to_skip = models.IntegerField(
        default=1,
    )
    
