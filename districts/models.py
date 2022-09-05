from django.db import models

# Create your models here.
#Okręgi
class District(models.Model):
    name = models.CharField(max_length=200)
    website = models.CharField(max_length=200, blank=True, null=True)
    id = models.IntegerField(unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


#Oddziały (mniejsze)
class Branch(models.Model):
    name = models.CharField(max_length=200)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    id = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
