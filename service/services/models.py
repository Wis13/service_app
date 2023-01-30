from django.db import models
from django.core.validators import MaxValueValidator
from services.tasks import set_price

from client.models import Client


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name} service"


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __str__(self):
        return f"Plan: {self.plan_type}"


class Subscription(models.Model):

    client = models.ForeignKey(Client, related_name='subscription', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscription', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscription', on_delete=models.PROTECT)
    price = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, save_mode=True, **kwargs):
        if save_mode:
            set_price.delay(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client}, service: {self.service}, {self.plan}"
