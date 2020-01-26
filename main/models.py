# Create your models here.
from django.db import models


class Profile(models.Model):
    TEAR_CHOICES = ((1, '아이언'),
                    (2, '브론즈'),
                    (3, '실버'),
                    (4, '골드'),
                    (5, '플래티넘'),
                    (6, '다이아'),
                    (7, '마스터'),
                    (8, '그랜드 마스터'),
                    (9, '챌린저'))
    tear = models.IntegerField(choices=TEAR_CHOICES)
    profile_id = models.CharField(max_length=30)
