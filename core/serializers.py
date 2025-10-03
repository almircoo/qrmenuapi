from rest_framework import serializers
from . import models


class PlaceDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Place
    fields = ('id', 'name', 'image', 'font', 'color', 'number_of_tables')

class PlaceSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Place
    fields = ('id', 'name', 'image')