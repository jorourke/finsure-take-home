from django.db import models


class Lender(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    upfront_commission_rate = models.FloatField()
    trial_commission_rate = models.FloatField()
    active = models.BooleanField(default=True)
