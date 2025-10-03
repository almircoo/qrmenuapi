from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Place(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  image = models.CharField(max_length=255)
  number_of_tables = models.IntegerField(default=1)
  font = models.CharField(max_length=100, blank=True)
  color = models.CharField(max_length=100, blank=True)

  def __str__(self):
    return "{}/{}".format(self.owner.username, self.name)
