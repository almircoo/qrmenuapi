from django.shortcuts import render
from rest_framework import generics
from . import models, serializers, permissions

# Create your views here.
class PlaceList(generics.ListCreateAPIView):
  serializer_class = serializers.PlaceSerializer

  def get_queryset(self):
    return models.Place.objects.filter(owner_id=self.request.user.id)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [permissions.IsOwnerOrReadOnly]
  serializer_class = serializers.PlaceDetailSerializer
  queryset = models.Place.objects.all()