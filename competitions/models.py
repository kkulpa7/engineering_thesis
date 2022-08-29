from django.db import models
from pigeons.models import Pigeon
import uuid

# Create your models here.
class Competition(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


class Category(models.Model):
    name = models.CharField(max_length=100)
    distance_min = models.IntegerField()
    distane_max = models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


class Results(models.Model):
    pigeon = models.ForeignKey(Pigeon, on_delete=models.CASCADE, null=True)
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, null=True)
    place = models.IntegerField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
