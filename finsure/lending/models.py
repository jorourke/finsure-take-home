from django.db import models
from model_utils.models import TimeStampedModel


class Lender(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    upfront_commission_rate = models.FloatField()
    trial_commission_rate = models.FloatField()
    active = models.BooleanField(default=True)
