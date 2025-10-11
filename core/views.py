from django.db import transaction
import json
import stripe
import decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
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

class CategoryList(generics.CreateAPIView):
  permission_classes = [permissions.PlaceOwnerOrReadOnly]
  serializer_class = serializers.CategorySerializer

class CategoryDetail(generics.UpdateAPIView, generics.DestroyAPIView):
  permission_classes = [permissions.PlaceOwnerOrReadOnly]
  serializer_class = serializers.CategorySerializer
  queryset = models.Category.objects.all()

class MenuItemList(generics.CreateAPIView):
  permission_classes = [permissions.PlaceOwnerOrReadOnly]
  serializer_class = serializers.MenuItemSerializer

class MenuItemDetail(generics.UpdateAPIView, generics.DestroyAPIView):
  permission_classes = [permissions.PlaceOwnerOrReadOnly]
  serializer_class = serializers.MenuItemSerializer
  queryset = models.MenuItem.objects.all()


def home(request):
  return render(request, 'index.html')

stripe.api_key = settings.STRIPE_API_SECRET_KEY
@csrf_exempt
@transaction.atomic # Ensure database operations are all or nothing
def create_payment_intent(request):
    try:
        # 1. Parse Data
        # Ensure we are handling only POST requests (good practice, though @csrf_exempt ignores method)
        if request.method != 'POST':
            return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

        data = json.loads(request.body)
        
        # Use Decimal for accurate currency handling
        amount_decimal = decimal.Decimal(str(data['amount'])) 
        amount_cents = int(amount_decimal * 100) # Stripe requires amount in cents (integer)
        
        # 2. Call Stripe API
        intent = stripe.PaymentIntent.create(
            amount = amount_cents,
            currency = 'usd',
            
            # 💡 FIX: data['payment_method'] is the string ID, not an object.
            payment_method = data['payment_method'], 
            
            off_session = True,
            confirm = True,
        )

        # 3. Create Order in Database
        order = models.Order.objects.create(
            place_id = data['place'],
            table = data['table'],
            detail = json.dumps(data['detail']),
            # Save the original float amount for the Order model
            amount = amount_decimal, 
            payment_intent = intent.id # Use intent.id as it's a better object property access
        )

        return JsonResponse({
            "success": True,
            "order": order.id,
            "payment_intent_status": intent.status
        })
        
    except stripe.error.CardError as e:
        # Handle card declines and other specific Stripe errors
        return JsonResponse({
            "success": False,
            "error": str(e.user_message),
        }, status=400)
    except json.JSONDecodeError:
        # Handle cases where the request body isn't valid JSON
        return JsonResponse({
            "success": False, 
            "error": "Invalid JSON format in request body."
        }, status=400)
    except KeyError as e:
        # Handle missing keys in the JSON payload
        return JsonResponse({
            "success": False, 
            "error": f"Missing required data field: {e}"
        }, status=400)
    except Exception as e:
        # Catch all other exceptions (including model validation, database issues)
        print(f"General error: {e}") # Log the specific error
        return JsonResponse({
            "success": False,
            "error": "An unexpected error occurred during processing.",
        }, status=500)
# @csrf_exempt
# def create_payment_intent(request):
#   try:
#     data = json.loads(request.body)
#     intent = stripe.PaymentIntent.create(
#       amount = data['amount'] * 100,
#       currency = 'usd',
#       payment_method = data['payment_method']['id'],
#       off_session = True,
#       confirm = True,
#     )

#     order = models.Order.objects.create(
#       place_id = data['place'],
#       table = data['table'],
#       detail = json.dumps(data['detail']),
#       amount = data['amount'],
#       payment_intent = intent['id']
#     )

#     return JsonResponse({
#       "success": True,
#       "order": order.id,
#     })
#   except Exception as e:
#     return JsonResponse({
#       "success": False,
#       "error": str(e),
#     })

class OrderList(generics.ListAPIView):
  serializer_class = serializers.OrderSerializer

  def get_queryset(self):
    return models.Order.objects.filter(place__owner_id=self.request.user.id, place_id=self.request.GET.get('place'))

class OrderDetail(generics.UpdateAPIView):
  permission_classes = [permissions.PlaceOwnerOrReadOnly]
  serializer_class = serializers.OrderSerializer
  queryset = models.Order.objects.all()