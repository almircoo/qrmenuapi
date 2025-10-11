import json
from rest_framework import permissions
from . import models

class IsOwnerOrReadOnly(permissions.BasePermission):
  
  def has_object_permission(self, request, view, obj):
    # Permisos de lectura permitidos para cualquier solicitud.
    if request.method in permissions.SAFE_METHODS:
        return True

    # Permisos de escritura solo permitidos al dueño del palce.
    return obj.owner == request.user

class PlaceOwnerOrReadOnly(permissions.BasePermission):
  
  def has_object_permission(self, request, view, obj):
    # Permisos de lectura permitidos para cualquier solicitud.
    if request.method in permissions.SAFE_METHODS:
        return True

    # Permisos de escritura solo permitidos al dueño del place relacionado.
    # Esto funciona para Category y MenuItem
    try:
        return obj.place.owner == request.user
    except AttributeError:
        # Manejar si el objeto no tiene el atributo 'place' directamente
        return False

  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
        return True # Permite la lectura (GET, HEAD, OPTIONS)
    
    if request.method in ['PUT', 'PATCH', 'DELETE']:
        # Solo exigimos que el usuario esté autenticado.
        return request.user and request.user.is_authenticated
    # Solo procedemos con la lógica de verificación si es una solicitud de escritura 
    if not request.user or not request.user.is_authenticated:
        return False # No autenticado

    # Para acciones de POST (Creación), intentamos extraer el ID del cuerpo.
    try:
        # Cargar los datos del cuerpo de la solicitud json
        data = json.loads(request.body)
    except json.JSONDecodeError:
        # Si el cuerpo no es JSON, usamos request.data
        data = request.data
    except Exception:
        return False # No se pudieron obtener los datos

    # LÓGICA CLAVE DE VERIFICACIÓN DE PERMISOS PARA CREACIÓN (POST):
    # 1
    if 'place' in data:
        place_id = data['place']
        try:
            # Verifica si el usuario actual es el dueño de ese Place
            return models.Place.objects.filter(pk=place_id, owner=request.user).exists()
        except ValueError: # Manejar si place_id no es un entero válido
            return False

    # 2 
    if 'category' in data:
        category_id = data['category']
        try:
            # Busca la Category, luego obtén su Place, y verifica el dueño
            return models.Category.objects.filter(
                pk=category_id, 
                place__owner=request.user # Usa doble guion bajo para seguir la relación
            ).exists()
        except ValueError: # Manejar si category_id no es un entero válido
            return False

    # Si la solicitud no tiene ni 'place' ni 'category' en los datos 
    return False