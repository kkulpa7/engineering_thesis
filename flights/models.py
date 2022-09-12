from django.db import models
from pigeons.models import Pigeon
from districts.models import District, Branch
import uuid

# Create your models here.
class Flight(models.Model):
    CATEGORY_CHOICES = (
        ('B', 'oddziałowe'),
        ('D', 'okręgowe')
    )

    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, null=True, blank=True)
    take_off_place = models.CharField(max_length=300, null=True, blank=True)
    # take_off_date = models.DateTimeField(null=True, blank=True)
    take_off_date = models.DateField(null=True, blank=True)
    pigeons_amount = models.IntegerField(null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.take_off_place

    class Meta:
        ordering = ['-take_off_date', 'take_off_place']


class Result(models.Model):
    pigeon = models.ForeignKey(Pigeon, on_delete=models.CASCADE, null=True)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, null=True)
    place = models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
