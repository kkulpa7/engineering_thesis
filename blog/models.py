from django.db import models
from django.utils import timezone
from users.models import Profile
import uuid

from django.db.models.deletion import CASCADE

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="default.jpg")
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    VOTE_TYPE = (
        ('up', 'pozytywny'),
        ('down', 'negatywny')
    )
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    value = models.CharField(max_length=5, choices=VOTE_TYPE)
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['author', 'post']]

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.name
