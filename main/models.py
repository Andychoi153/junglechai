# Create your models here.
from django.db import models


class Profile(models.Model):
    TEAR_CHOICES = ((1, '일반'))
    tear = models.IntegerField(choices=TEAR_CHOICES)
    lol_id = models.CharField(max_length=30)
