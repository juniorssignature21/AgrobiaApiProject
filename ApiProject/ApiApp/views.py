from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, CartItem, Order, Category
from .serializers import UserSerializer, ProductSerializer, CartItemSerializer, OrderSerializer, CategorySerializer
from django.contrib.auth.models import User
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import paypalrestsdk
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

@csrf_exempt
def create_payment(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            print("Request Body:", body)  # Debug print

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": "http://localhost:8000/api/payment/execute/",
                    "cancel_url": "http://localhost:8000/api/payment/cancel/"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": "Farm Produce",
                            "sku": "001",
                            "price": "10.00",
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": "10.00",
                        "currency": "USD"
                    },
                    "description": "Payment for farm produce"
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = str(link.href)
                        return JsonResponse({"approval_url": approval_url})
            else:
                print("Payment Error:", payment.error)  # Debug print
                return JsonResponse({"error": payment.error}, status=400)
        except Exception as e:
            print("Exception:", str(e))  # Debug print
            return JsonResponse({"error": str(e)}, status=400)
    else:
        print("Invalid request method")  # Debug print
        return HttpResponseBadRequest("Invalid request method.")
    
@csrf_exempt
def execute_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get("paymentId")
        payer_id = request.POST.get("PayerID")

        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            return JsonResponse({"status": "Payment executed successfully"})
        else:
            return JsonResponse({"error": payment.error}, status=400)
    return HttpResponseBadRequest("Invalid request method.")


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProductUploadView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddToCartView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class CartItemListView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(buyer=self.request.user)

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
