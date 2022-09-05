from django.db import models
from django.utils import timezone
from users.models import Profile
from taggit.managers import TaggableManager
import uuid

from django.db.models.deletion import CASCADE


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    @property
    def getVoteCount(self):
        comments = self.comments.all()
        upVotes = comments.filter(value='up').count()
        totalVotes = comments.count()

        ratio = (upVotes / totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

    @property
    def commentators(self):
        queryset = self.comments.all().values_list('author__id', flat=True)
        return queryset


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
