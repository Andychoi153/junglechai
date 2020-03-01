# Create your models here.
from django.db import models


class Profile(models.Model):
    TEAR_CHOICES = ((0, '아이언'),
                    (1, '브론즈'),
                    (2, '실버'),
                    (3, '골드'),
                    (4, '플래티넘 3-4'),
                    (5, '플래티넘 2'),
                    (6, '플래티넘 1'),
                    (7, '다이아 4'),
                    (8, '다이아 3'),
                    (9, '다이아 2'),
                    (10, '다이아1'),
                    (11, '마스터'),
                    (12, '그랜드 마스터'),
                    (13, '챌린저'),)
    tier = models.IntegerField(choices=TEAR_CHOICES)
    lol_id = models.CharField(max_length=30)
