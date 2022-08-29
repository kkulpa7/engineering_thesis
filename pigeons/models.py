from django.db import models
from django.utils import timezone
from users.models import Profile
import uuid

# Create your models here.


class Pigeon(models.Model):
    GENDER_CHOICES = (
        ('F', 'samica'),
        ('M', 'samiec')
    )
    STATUS_CHOICES = (
        ('L', 'loty'),
        ('R', 'rozpłód'),
        ('A', 'archiwum'),
        ('M', 'martwy')
    )

    number = models.CharField(max_length=30)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="selfMother", limit_choices_to={'gender': 'F'})
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="selfFather", limit_choices_to={'gender': 'M'})
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, blank=True)

    image_body = models.ImageField(null=True, blank=True, upload_to='pigeons/body')
    image_wing = models.ImageField(null=True, blank=True, upload_to='pigeons/wing')
    image_eye = models.ImageField(null=True, blank=True, upload_to='pigeons/eye')

    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)


    death_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['-created']


class Color(models.Model):
    color_long = models.CharField(max_length=50)
    color_short = models.CharField(max_length=5)
    color_esk = models.CharField(max_length=5)
    id = models.IntegerField(unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.color_long

    class Meta:
        ordering = ['color_long']
