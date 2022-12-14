from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from districts.models import Branch

import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, unique=True, blank=True, null=True)
    # phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/profile-default.jpg')
    bio = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    street = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=6, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.username)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    sender_2 = models.CharField(max_length=200, null=True, blank=True)
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    subject = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
